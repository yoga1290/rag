from yoga1290.rag.domain.models.classification import Classification
from yoga1290.rag.domain.models.parsed_document import ParsedDocument
from yoga1290.rag.domain.schemas.classification_schema import ClassificationSchema


class DocumentClassifier():
    """
    Classifies a document according to a domain-defined classification schema.

    Implementations may use:
      - Databricks ai_classify
      - Qwen
      - BERT
      - Other classifiers
    """
    def classify(
        self,
        document: ParsedDocument,
        schema: ClassificationSchema,
    ) -> Classification:
        """
        Classify a document.

        Args:
            document: Parsed document.
            schema: Allowed categories and classification configuration.

        Returns:
            Classification result.
        """
        raise NotImplementedError