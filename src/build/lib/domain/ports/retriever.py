from abc import ABC, abstractmethod
from collections.abc import Sequence

from yoga1290.rag.domain.models.chunk import Chunk


class Retriever(ABC):

    @abstractmethod
    def retrieve(
        self,
        query: str,
        *,
        top_k: int = 2,
    ) -> Sequence[Chunk]:
        raise NotImplementedError