from yoga1290.rag.domain.models.parsed_document import ParsedDocument
from yoga1290.rag.domain.models.search_document import SearchDocument

class SearchPreparer():
    """
    Prepares parsed documents for semantic/hybrid search.

    Implementations may use:
      - Databricks ai_prep_search
      - Custom chunking
      - Recursive text splitting
      - Layout-aware chunking
      - Semantic chunking
    """
    def prepare(self, document: ParsedDocument) -> SearchDocument:
        """
        Prepare a parsed document for search/indexing.

        Args:
            document: Parsed document.

        Returns:
            Search-ready document containing chunks and metadata.
        """
        raise NotImplementedError