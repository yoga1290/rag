from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter

from yoga1290.rag.domain.models.chunk import Chunk
from yoga1290.rag.domain.models.parsed_document import ParsedDocument
from yoga1290.rag.domain.models.search_document import SearchDocument
from yoga1290.rag.domain.ports.search_preparer import SearchPreparer
import os

class RecursiveCharacterSearchPreparer(SearchPreparer):
    """
    Local SearchPreparer implementation using LangChain's
    RecursiveCharacterTextSplitter.
    """

    def __init__(
        self,
        chunk_size=int(os.getenv('TEXT_SPLITTER_CHUNK_SIZE', '500')),
        chunk_overlap=int(os.getenv('TEXT_SPLITTER_CHUNK_OVERLAP', '50')),
    ) -> None:
        self._text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

    def prepare(
        self,
        document: ParsedDocument,
    ) -> SearchDocument:

        if not document.text:
            raise ValueError(
                f"text is missing for ParsedDocument "
                f"{document.document_id}"
            )
        
        texts = self._text_splitter.split_text(document.text)

        chunks = tuple(
            Chunk(
                id=f"{document.document_id}-chunk-{index}",
                document_id=document.document_id,
                text=text,
                index=index,
                metadata={
                    "chunk_index": index,
                },
            )
            for index, text in enumerate(texts)
        )

        return SearchDocument(
            document_id=document.document_id,
            chunks=chunks,
            metadata={
                "splitter": "recursive_character",
                "chunk_size": self._text_splitter._chunk_size,
                "chunk_overlap": self._text_splitter._chunk_overlap,
            },
        )