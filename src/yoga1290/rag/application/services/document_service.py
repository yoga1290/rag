from yoga1290.rag.domain.ports.document_parser import DocumentParser
from yoga1290.rag.domain.ports.document_source import DocumentSource

class DocumentService:
    def __init__(
        self,
        source: DocumentSource,
        parser: DocumentParser,
    ) -> None:
        self.source = source
        self.parser = parser

    def process(self, document_id: str):
        document = self.source.get(document_id)
        return self.parser.parse(document)
