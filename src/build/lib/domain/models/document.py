from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Mapping

@dataclass(frozen=True, slots=True)
class Document:
    id: str | None = None
    size_bytes: int | None = None
    uri: str | None = None
    content: bytes | None = None
    filename: str = None
    content_type: str = None
    metadata: Mapping[str, object] = field(default_factory=dict)
    created_at: datetime | None = None

    @property
    def suffix(self) -> str:
        return Path(self.filename).suffix.lower()