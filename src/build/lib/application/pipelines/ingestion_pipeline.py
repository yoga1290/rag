from yoga1290.rag.domain.models import (
                            Document,
                            ParsedDocument,
                            SearchDocument)
from yoga1290.rag.domain.ports import (
                            DocumentParser,
                            DocumentExtractor,
                            DocumentClassifier,
                            SearchPreparer,
                            VectorStore,)
from collections.abc import Sequence

class IngestionPipeline:
    def __init__(
        self,
        parser: DocumentParser,
        extractor: DocumentExtractor,
        classifier: DocumentClassifier,
        search_preparer: SearchPreparer,
        vectorstore: VectorStore,
    ) -> None:
        self.parser = parser
        self.extractor = extractor
        self.classifier = classifier
        self.search_preparer = search_preparer
        self.vectorstore = vectorstore
    
    def process(self,
                documents: Sequence[Document],
                # extraction_schema,
                # classification_schema,
        ):
        search_documents = []
        for document in documents:
            parsed_document: ParsedDocument = (
                                self.parser.parse(document))
            search_document: SearchDocument = (
                                self.search_preparer.prepare(parsed_document))
            search_documents.append(search_document)
        self.vectorstore.add_documents(search_documents)

        return {
            # "parsed": parsed,
            # "extracted": extracted,
            # "classification": classification,
            "search_document": search_documents,
        }


        # extracted = self.extractor.extract(parsed, extraction_schema)
        # classification = self.classifier.classify(
        #     parsed,
        #     classification_schema,
        # )
