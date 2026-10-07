from typing import Any

from pydantic import BaseModel

from yoga1290.rag.domain.models import (
    ParsedDocument,
    ExtractedData,
)
from yoga1290.rag.domain.ports import DocumentExtractor
from yoga1290.rag.factories import LLMFactory


class ExtractionResult(BaseModel):
    value: str | None #TODO


class LlamaCppMistralDocumentExtractor(DocumentExtractor):

    def __init__(self):
        self._llm = LLMFactory.createLocalLlamaCppLLM()

    def extract(
        self,
        parsed_document: ParsedDocument,
        fields: list[str],
    ) -> ExtractedData:

        extracted: dict[str, Any] = {}

        prompt = self._build_prompt(
                document=parsed_document.text,
                field=', '.join(fields),
            )
        response = self._llm.generate(
                prompt=prompt,
            )
        return ExtractedData(
            document_id=parsed_document.document_id,
            data=self.mapResponseToFieldValueDict(response),
            provider="LlamaCppDocumentExtractor",
        )

    @staticmethod
    def _build_prompt(
        document: str,
        field: str,
    ) -> str:

        return f"""
From the provided document below, FIND and LIST the VALUES of {field}, print one value per line.
DOCUMENT: {document}
VALUES:
""".strip()

    @staticmethod
    def mapResponseToFieldValueDict(text: str) -> dict[str, str]:
        import re
        result = {}

        for line in text.splitlines():
            line = line.strip()

            if not line:
                continue

            match = re.match(r"^[\s\*]*([^:]+)[\s\*]*\:[\s\*]*([^:]+)[\s\*]*$", line)

            if match:
                field, value = match.groups()
                result[field.strip()] = value.strip()

        return result