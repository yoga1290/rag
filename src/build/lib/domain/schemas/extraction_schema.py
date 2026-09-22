from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


@dataclass(frozen=True, slots=True)
class ExtractionField:
    name: str
    description: str | None = None
    required: bool = False


class ExtractionSchema(Generic[T]):

    def __init__(
        self,
        fields: list[ExtractionField] | None = None,
        model: type[T] | None = None,
        description: str | None = None,
    ) -> None:
        self.fields = tuple(fields)
        self.model = model
        self.description = description

    @property
    def field_names(self) -> tuple[str, ...]:
        return tuple(field.name for field in self.fields)

    def as_prompt(self) -> str:
        """
        Provider-independent textual representation that can
        be used by local LLM implementations.
        """
        lines = []

        for field in self.fields:
            description = field.description or ""
            required = "required" if field.required else "optional"

            lines.append(
                f"- {field.name}: {description} ({required})"
            )

        return "\n".join(lines)