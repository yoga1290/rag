from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True, slots=True)
class Chunk:
    id: str
    document_id: str
    text: str
    index: int
    embedding: Sequence[float] | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)
