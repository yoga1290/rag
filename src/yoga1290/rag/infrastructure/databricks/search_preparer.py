from yoga1290.rag.domain.models.search_document import SearchDocument
from yoga1290.rag.domain.ports.search_preparer import SearchPreparer

class DatabricksSearchPreparer(SearchPreparer):
    def prepare(self, document) -> SearchDocument:
        raise NotImplementedError(
            "Implement using Databricks ai_prep_search()."
        )
