from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from .chunk import Chunk

@dataclass(frozen=True, slots=True)
class SearchDocument:
    document_id: str
    chunks: Sequence[Chunk] = field(default_factory=tuple)
    metadata: Mapping[str, object] = field(default_factory=dict)

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)
