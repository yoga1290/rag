from yoga1290.rag.domain.models.classification import Classification
from yoga1290.rag.domain.ports.document_classifier import DocumentClassifier

class DatabricksDocumentClassifier(DocumentClassifier):
    def classify(self, document, schema) -> Classification:
        raise NotImplementedError(
            "Implement using Databricks ai_classify()."
        )
