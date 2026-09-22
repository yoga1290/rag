from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True, slots=True)
class ClassificationSchema:
    categories: Sequence[str]
    description: str | None = None
    multi_label: bool = False
