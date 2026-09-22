from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

@dataclass(frozen=True, slots=True)
class SearchResult:
    chunk_id: str
    document_id: str
    text: str
    score: float
    metadata: Mapping[str, object] = field(default_factory=dict)
