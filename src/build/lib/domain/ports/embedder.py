from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence


class Embedder(ABC):
    """
    Port for generating vector embeddings from text.

    Implementations may use local models, Databricks models,
    Hugging Face models, or remote embedding APIs.
    """

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimensionality of the generated embeddings.
        """
        raise NotImplementedError

    @abstractmethod
    def embed(self, text: str) -> list[float]:
        """
        Generate an embedding for a single piece of text.

        Args:
            text: Text to embed.

        Returns:
            Embedding vector.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: Texts to embed.

        Returns:
            Embedding vectors in the same order as the input.
        """
        raise NotImplementedError
        
    @abstractmethod
    def embed_batch(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: Texts to embed.

        Returns:
            Embedding vectors in the same order as the input.
        """
        raise NotImplementedError
