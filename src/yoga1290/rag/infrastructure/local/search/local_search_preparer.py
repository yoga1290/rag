from yoga1290.rag.domain.models.search_document import SearchDocument
from yoga1290.rag.domain.ports.search_preparer import SearchPreparer
from .recursive_character_search_preparer import RecursiveCharacterSearchPreparer
import os

class LocalSearchPreparer(SearchPreparer):

    def __init__(
        self,
        chunk_size:int = int(os.getenv(
            "TEXT_SPLITTER_CHUNK_SIZE",
            "500",
        )),
        chunk_overlap:int = int(os.getenv(
            "TEXT_SPLITTER_CHUNK_OVERLAP",
            "50",
        )),
    ) -> None:

        self.recursive_character_search_preparer = RecursiveCharacterSearchPreparer(
                    chunk_size= chunk_size,
                    chunk_overlap= chunk_overlap,
                )
        
    def prepare(self, document) -> SearchDocument:

        return self.recursive_character_search_preparer.prepare(
                    document=document
                )


