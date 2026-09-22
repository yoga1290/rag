from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Source:
    document_id: str
    chunk_id: str
    metadata: dict[str, Any]


@dataclass(frozen=True, slots=True)
class RagResult:
    question: str
    answer: str
    sources: tuple[Source, ...]
    duration_seconds: float