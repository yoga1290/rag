from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")

@dataclass(frozen=True, slots=True)
class ExtractedData(Generic[T]):
    document_id: str
    data: T
    confidence: float | None = None
    provider: str | None = None
    extracted_at: datetime | None = None
