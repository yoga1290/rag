from yoga1290.rag.domain.models.document import Document
from yoga1290.rag.domain.models.parsed_document import ParsedDocument

class DocumentParser():
    """
    Converts a raw document into a normalized ParsedDocument.

    Implementations may use:
      - Databricks ai_parse_document
      - Docling
      - PyMuPDF
      - OCR
      - Other document parsing engines
    """
    def parse(self, document: Document) -> ParsedDocument:
        """
        Parse a document into a normalized representation.

        Args:
            document: Raw document metadata and content reference.

        Returns:
            ParsedDocument containing normalized text, pages,
            tables, images, metadata, etc.

        Raises:
            DocumentParseError: If the document cannot be parsed.
        """
        raise NotImplementedError

