from __future__ import annotations

import os
from typing import Any
from yoga1290.rag.domain.models import SearchDocument
from yoga1290.rag.domain.ports.embedder import Embedder
from yoga1290.rag.domain.ports.vector_store import VectorStore

from .pgvector_retriever import PGVectorRetriever

class PGVectorStore(VectorStore):
    """
    Local PostgreSQL + pgvector implementation.

    Converts domain SearchDocument objects into LangChain
    Documents internally before passing them to PGVector.
    """

    ####
    from langchain_core.documents import Document as LangChainDocument
    ###


    def __init__(
        self,
        embedder: Embedder,
        connection_string: str | None = None,
        collection_name: str = "knowledge_base",
    ) -> None:

        from langchain_core.retrievers import BaseRetriever
        from langchain_postgres import PGVector

        self._embedder = embedder

        self._connection_string = (
            connection_string
            or self._build_connection_string()
        )

        self._collection_name = collection_name

        self._vectorstore = PGVector(
            connection=self._connection_string,
            embeddings=embedder,
            collection_name=self._collection_name,
        )

    def add_documents(
        self,
        documents: Sequence[SearchDocument],
    ) -> list[str]:
        """
        Store all chunks from a SearchDocument.

        PGVector will generate embeddings through the injected
        Embedder and persist the resulting vectors and metadata.
        """

        # if not document.chunks:
        #     return []
        print(f'documents len: {len(documents)}')
        print(f'documents[0].chunks len: {len(documents[0].chunks)}')

        langchain_documents, chunk_ids = (
            self._to_langchain_documents(documents)
        )

        print(f'chunk_ids: {chunk_ids} {len(chunk_ids)}')
        print(f'langchain_documents len: {len(langchain_documents)}')

        return self._vectorstore.add_documents(
            langchain_documents,
            ids= chunk_ids
        )

    def as_retriever(
        self,
        *,
        search_kwargs: dict[str, Any] | None = None,
    ) -> BaseRetriever: #TODO

        if search_kwargs is None:
            search_kwargs = {}

        return self._vectorstore.as_retriever(
            search_kwargs=search_kwargs
        )

    @staticmethod
    def _build_connection_string() -> str:

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        database = os.getenv("POSTGRES_DB")

        if not user:
            raise ValueError(
                "POSTGRES_USER is not configured"
            )

        if not password:
            raise ValueError(
                "POSTGRES_PASSWORD is not configured"
            )

        if not database:
            raise ValueError(
                "POSTGRES_DB is not configured"
            )

        return (
            "postgresql+psycopg://"
            f"{user}:{password}"
            "@postgres:5432/"
            f"{database}"
        )

    @staticmethod
    def _to_langchain_documents(
        search_documents: Sequence[SearchDocument],
    ) -> tuple[list[LangChainDocument], list[str]]:
        """
        Convert a domain SearchDocument into LangChain Documents.

        One domain Chunk becomes one LangChain Document.
        """
        from langchain_core.documents import Document as LangChainDocument

        ids: list[str] = []
        langchain_documents: list[LangChainDocument] = []

        for search_document in search_documents:
            for chunk in search_document.chunks:

                if not chunk.id:
                    raise ValueError(
                        f"Chunk ID is missing for document "
                        f"{search_document.document_id}"
                    )
                
                ids.append(chunk.id)

                metadata = {
                    # Domain-level metadata
                    **search_document.metadata,

                    # Chunk-level metadata
                    **chunk.metadata,

                    # Canonical identifiers
                    "document_id": search_document.document_id,
                    "chunk_id": chunk.id,
                    "chunk_index": chunk.index,
                }

                langchain_documents.append(
                    LangChainDocument(
                        page_content=chunk.text,
                        metadata=metadata,
                    )
                )


        return langchain_documents, ids