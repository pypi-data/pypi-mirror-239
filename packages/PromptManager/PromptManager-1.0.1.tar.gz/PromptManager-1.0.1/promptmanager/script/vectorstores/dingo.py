from __future__ import annotations

import logging
import uuid
from typing import Any, Iterable, List, Optional, Tuple

from promptmanager.runtime.exception import flow_exception
from promptmanager.script.schema.document import PMDocument
from promptmanager.script.schema.embeddings import PMEmbeddings
from promptmanager.script.schema.vectordb import PMVectorDB

logger = logging.getLogger('pm_log')


class Dingo(PMVectorDB):

    def __init__(
            self,
            embedding: PMEmbeddings,
            text_key: str,
            *,
            client: Any = None,
            index_name: Optional[str] = None,
            host: Optional[List[str]] = None,
            user: str = "root",
            password: str = "123123",
            self_id: bool = False,
    ):
        """Initialize with Dingo client."""
        try:
            import dingodb
        except ImportError:
            raise ImportError(
                "Could not import dingo python package. "
                "Please install it with `pip install dingodb."
            )

        host = host if host is not None else ["172.20.31.10:13000"]

        # collection
        if client is not None:
            dingo_client = client
        else:
            try:
                # connect to dingo db
                dingo_client = dingodb.DingoDB(user, password, host)
            except ValueError as e:
                raise ValueError(f"Dingo failed to connect: {e}")

        self._text_key = text_key
        self._client = dingo_client

        if index_name is not None and index_name not in dingo_client.get_index():
            if self_id is True:
                dingo_client.create_index(index_name, 1024, auto_id=False)
            else:
                dingo_client.create_index(index_name, 1024)

        self._index_name = index_name
        self._embedding = embedding

    @property
    def embeddings(self) -> Optional[PMEmbeddings]:
        return self._embedding

    def add_texts(
            self,
            texts: Iterable[str],
            metadatas: Optional[List[dict]] = None,
            ids: Optional[List[str]] = None,
            text_key: str = "text",
            batch_size: int = 500,
            **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectorstore.

        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            ids: Optional list of ids to associate with the texts.

        Returns:
            List of ids from adding the texts into the vectorstore.

        """

        # Embed and create the documents
        ids = ids or [str(uuid.uuid1().int)[:13] for _ in texts]
        metadatas_list = []
        texts = list(texts)
        embeds = self._embedding.embed_documents(texts)
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            metadata[self._text_key] = text
            metadatas_list.append(metadata)
        # upsert to Dingo
        for i in range(0, len(list(texts)), batch_size):
            j = i + batch_size
            add_res = self._client.vector_add(
                self._index_name, metadatas_list[i:j], embeds[i:j], ids[i:j]
            )
            if not add_res:
                raise Exception("vector add fail")

        return ids

    def similarity_search(
            self,
            query: str,
            k: int = 4,
            search_params: Optional[dict] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[PMDocument]:
        """Return Dingo documents most similar to query, along with scores.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            search_params: Dictionary of argument(s) to filter on metadata

        Returns:
            List of Documents most similar to the query and score for each
        """
        docs_and_scores = self.similarity_search_with_score(
            query, k=k, search_params=search_params
        )
        return [doc for doc, _ in docs_and_scores]

    def similarity_search_with_score(
            self,
            query: str,
            k: int = 4,
            search_params: Optional[dict] = None,
            timeout: Optional[int] = None,
            **kwargs: Any,
    ) -> List[Tuple[PMDocument, float]]:
        """Return Dingo documents most similar to query, along with scores.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            search_params: Dictionary of argument(s) to filter on metadata

        Returns:
            List of Documents most similar to the query and score for each
        """
        docs = []
        query_obj = self._embedding.embed_query(query)
        results = self._client.vector_search(
            self._index_name, xq=query_obj, top_k=k, search_params=search_params
        )

        logger.info("-------query dingo result:")
        logger.info(results)

        if isinstance(results, dict):
            if results['status'] == 500:
                raise flow_exception.DINGO_QUERY_ERROR(message=results['message'])
            results = results['data']

        if not results:
            return []

        for res in results[0]["vectorWithDistances"]:
            metadatas = res["scalarData"]
            id = res["id"]
            score = res["distance"]
            text = metadatas[self._text_key]["fields"][0]["data"]

            metadata = {"id": id, "text": text, "score": score}
            docs.append((PMDocument(page_content=text, metadata=metadata), score))

        return docs

    def max_marginal_relevance_search(
            self,
            query: str,
            k: int = 4,
            fetch_k: int = 20,
            lambda_mult: float = 0.5,
            search_params: Optional[dict] = None,
            **kwargs: Any,
    ) -> List[PMDocument]:
        """Return docs selected using the maximal marginal relevance.

        Maximal marginal relevance optimizes for similarity to query AND diversity
        among selected documents.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            fetch_k: Number of Documents to fetch to pass to MMR algorithm.
            lambda_mult: Number between 0 and 1 that determines the degree
                        of diversity among the results with 0 corresponding
                        to maximum diversity and 1 to minimum diversity.
                        Defaults to 0.5.
        Returns:
            List of Documents selected by maximal marginal relevance.
        """
        embedding = self._embedding.embed_query(query)
        return self.max_marginal_relevance_search_by_vector(
            embedding, k, fetch_k, lambda_mult, search_params
        )

    @classmethod
    def from_texts(
            cls,
            texts: List[str],
            embedding: PMEmbeddings,
            metadatas: Optional[List[dict]] = None,
            ids: Optional[List[str]] = None,
            text_key: str = "text",
            index_name: Optional[str] = None,
            client: Any = None,
            host: List[str] = ["172.20.31.10:13000"],
            user: str = "root",
            password: str = "123123",
            batch_size: int = 500,
            **kwargs: Any,
    ) -> Dingo:
        """Construct Dingo wrapper from raw documents.

                This is a user friendly interface that:
                    1. Embeds documents.
                    2. Adds the documents to a provided Dingo index

                This is intended to be a quick way to get started.

                Example:
                    .. code-block:: python

                        from promptmanager.script.base.vectorstores import Dingo
                        from promptmanager.script.base.embeddings import OpenAIEmbeddings
                        import dingodb
        sss
                        embeddings = OpenAIEmbeddings()
                        dingo = Dingo.from_texts(
                            texts,
                            embeddings,
                            index_name="promptmanager-demo"
                        )
        """
        try:
            import dingodb
        except ImportError:
            raise ImportError(
                "Could not import dingo python package. "
                "Please install it with `pip install dingodb`."
            )

        if client is not None:
            dingo_client = client
        else:
            try:
                # connect to dingo db
                dingo_client = dingodb.DingoDB(user, password, host)
            except ValueError as e:
                raise ValueError(f"Dingo failed to connect: {e}")
        if kwargs is not None and kwargs.get("self_id") is True:
            if index_name not in dingo_client.get_index():
                dingo_client.create_index(index_name, 1024, auto_id=False)
        else:
            if index_name not in dingo_client.get_index():
                dingo_client.create_index(index_name, 1024)
            # dingo_client.create_index(index_name, 1024, index_type="hnsw")

        # Embed and create the documents

        ids = ids or [str(uuid.uuid1().int)[:13] for _ in texts]
        metadatas_list = []
        texts = list(texts)
        embeds = embedding.embed_documents(texts)
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            metadata[text_key] = text
            metadatas_list.append(metadata)

        # upsert to Dingo
        for i in range(0, len(list(texts)), batch_size):
            j = i + batch_size
            add_res = dingo_client.vector_add(
                index_name, metadatas_list[i:j], embeds[i:j], ids[i:j]
            )
            if not add_res:
                raise Exception("vector add fail")
        return cls(embedding, text_key, client=dingo_client, index_name=index_name)

    def delete(
            self,
            ids: Optional[List[str]] = None,
            **kwargs: Any,
    ) -> Any:
        """Delete by vector IDs or filter.
        Args:
            ids: List of ids to delete.
        """

        if ids is None:
            raise ValueError("No ids provided to delete.")

        return self._client.vector_delete(self._index_name, ids=ids)
