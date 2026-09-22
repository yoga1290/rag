from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from yoga1290.rag.domain.models.extracted_data import ExtractedData
from yoga1290.rag.domain.models.parsed_document import ParsedDocument
from yoga1290.rag.domain.schemas.extraction_schema import ExtractionSchema

T = TypeVar("T")

class DocumentExtractor(ABC, Generic[T]):
    @abstractmethod
    def extract(
        self,
        document: ParsedDocument,
        schema: ExtractionSchema[T],
    ) -> ExtractedData[T]:
        raise NotImplementedError
