import re
from difflib import SequenceMatcher
from typing import Any

from yoga1290.rag.domain.models import (
    ParsedDocument,
    ExtractedData,
)
from yoga1290.rag.domain.ports import DocumentExtractor
from yoga1290.rag.factories import LLMFactory


class LlamaCppDocumentExtractor(DocumentExtractor):

    def __init__(self):
        self._llm = LLMFactory.createLocalLlamaCppLLM()

    def extract(
        self,
        parsed_document: ParsedDocument,
        fields: list[str],
    ) -> ExtractedData:

        prompt = f"""
Extract the values of the requested fields from the document.

REQUESTED FIELDS:
{chr(10).join(f"- {field}" for field in fields)}

DOCUMENT:
{parsed_document.text}

OUTPUT:
Write one field and its value on each line.

Use this format:

{{FIELD}}: {{VALUE}}

RULES:
- Extract only the requested fields.
- Do not explain your answer.
- Do not write Python code.
- Do not write JSON.
- Do not write Markdown.
- Do not provide examples.
- Do not repeat the document.
- If a value cannot be found, write null.
"""

        response = self._llm.generate(prompt)

        data = self._parse_response(
            response=response,
            fields=fields,
        )

        return ExtractedData(
            document_id=parsed_document.document_id,
            data=data,
            provider="LlamaCppDocumentExtractor",
        )

    @staticmethod
    def _normalize_field_name(value: str) -> str:
        """
        Normalize field names so that:

            field_name
            field-name
            field name

        all become:

            field name
        """
        value = value.lower().strip()
        value = re.sub(r"[_\-]+", " ", value)
        value = re.sub(r"\s+", " ", value)
        return value

    @staticmethod
    def _similarity(left: str, right: str) -> float:
        return SequenceMatcher(
            None,
            LlamaCppDocumentExtractor._normalize_field_name(left),
            LlamaCppDocumentExtractor._normalize_field_name(right),
        ).ratio()

    @classmethod
    def _find_field(
        cls,
        field_name: str,
        requested_fields: list[str],
    ) -> str | None:

        normalized = cls._normalize_field_name(field_name)

        # First try exact normalized matching.
        for requested in requested_fields:
            if normalized == cls._normalize_field_name(requested):
                return requested

        # Then tolerate small spelling differences.
        best_field = None
        best_score = 0.0

        for requested in requested_fields:
            score = cls._similarity(field_name, requested)

            if score > best_score:
                best_score = score
                best_field = requested
        # Don't accept a very weak fuzzy match.
        if best_score >= 0.75:
            return best_field

        return None

    @classmethod
    def _parse_response(
        cls,
        response: str,
        fields: list[str],
    ) -> dict[str, Any]:

        # Start with every requested field.
        # This guarantees that missing fields are returned as None.
        extracted: dict[str, Any] = {
            field: None
            for field in fields
        }

        for line in response.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove common Markdown list markers.
            line = re.sub(r"^[-*]\s+", "", line)

            # We only care about lines containing:
            #
            # field: value
            #
            if ":" not in line:
                continue

            field_name, value = line.split(":", 1)

            field_name = field_name.strip()
            value = value.strip()

            # Ignore obvious non-field lines.
            if not field_name:
                continue

            # Find the requested field that this generated field
            # most closely corresponds to.

            requested_field = field_name
            requested_field = cls._find_field(
                field_name,
                fields,
            )
            if requested_field is None:
                continue

            # Don't allow a later duplicate generated field
            # to overwrite the first useful value.
            if extracted.get(requested_field) is not None:
                continue

            # Normalize missing values.
            if value.lower() in {
                "null",
                "none",
                "n/a",
                "not found",
                "unknown",
            }:
                value = None

            extracted[requested_field] = value

        return extracted