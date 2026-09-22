from yoga1290.rag.domain.models.document import Document
from yoga1290.rag.domain.models.parsed_document import ParsedDocument
from yoga1290.rag.domain.ports.document_parser import DocumentParser

class DatabricksDocumentParser(DocumentParser):
    def parse(self, document: Document) -> ParsedDocument:
        raise NotImplementedError(
            "Implement using Databricks ai_parse_document()."
        )
