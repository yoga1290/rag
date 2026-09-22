from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Sequence

from yoga1290.rag.domain.models.search_document import SearchDocument

class VectorStore(ABC):
    """
    Port for vector storage and similarity retrieval.

    Implementations may use PGVector, Milvus, Chroma,
    Databricks Vector Search, etc.
    """

    @abstractmethod
    def add_documents(
        self,
        documents: Sequence[SearchDocument],
    ) -> list[str]:
        """
        Add documents to the vector store.

        Args:
            documents: Documents/chunks to embed and store.

        Returns:
            IDs of the added documents.
        """
        raise NotImplementedError

    @abstractmethod
    def as_retriever(
        self,
        *,
        search_kwargs: dict[str, Any] | None = None,
    ) -> Any:
        """
        Create a retriever backed by this vector store.

        Example:
            retriever = store.as_retriever(
                search_kwargs={"k": 5}
            )
        """
        raise NotImplementedError