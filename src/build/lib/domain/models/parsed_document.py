from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True, slots=True)
class ParsedPage:
    page_number: int
    text: str
    metadata: Mapping[str, object] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class ParsedTable:
    table_id: str
    page_number: int | None
    headers: Sequence[str] = field(default_factory=tuple)
    rows: Sequence[Sequence[object]] = field(default_factory=tuple)
    metadata: Mapping[str, object] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class ParsedDocument:
    document_id: str
    text: str
    pages: Sequence[ParsedPage] = field(default_factory=tuple)
    tables: Sequence[ParsedTable] = field(default_factory=tuple)
    metadata: Mapping[str, object] = field(default_factory=dict)

    @property
    def page_count(self) -> int:
        return len(self.pages)