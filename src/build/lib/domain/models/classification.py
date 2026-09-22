from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

@dataclass(frozen=True, slots=True)
class ClassificationLabel:
    name: str
    confidence: float | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class Classification:
    document_id: str
    labels: Sequence[ClassificationLabel]
    provider: str | None = None

    @property
    def primary_label(self) -> ClassificationLabel | None:
        return self.labels[0] if self.labels else None
