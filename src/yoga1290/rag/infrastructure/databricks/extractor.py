from yoga1290.rag.domain.models.extracted_data import ExtractedData
from yoga1290.rag.domain.models.parsed_document import ParsedDocument
from yoga1290.rag.domain.ports.document_extractor import DocumentExtractor

class DatabricksDocumentExtractor(DocumentExtractor):
    def extract(self, document, schema) -> ExtractedData:
        raise NotImplementedError(
            "Implement using Databricks ai_extract()."
        )
