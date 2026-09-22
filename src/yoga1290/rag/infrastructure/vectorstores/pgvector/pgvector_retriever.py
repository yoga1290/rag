from collections.abc import Sequence

from yoga1290.rag.domain.models import Chunk
from yoga1290.rag.domain.ports import Retriever


class PGVectorRetriever(Retriever):

    from langchain_core.documents import Document as LangChainDocument

    def __init__(
        self,
        vectorstore,
        top_k: int = 2,
    ) -> None:
        self._vectorstore = vectorstore
        self._top_k = top_k

    def retrieve(
        self,
        query: str,
        *,
        top_k: int | None = None,
    ) -> Sequence[Chunk]:

        k = top_k or self._top_k

        retriever = self._vectorstore.as_retriever(
            search_kwargs={"k": k}
        )

        documents: list[LangChainDocument] = retriever.invoke(query)

        return tuple(
            Chunk(
                id=document.metadata["chunk_id"],
                document_id=document.metadata["document_id"],
                text=document.page_content,
                index=document.metadata.get("chunk_index", 0),
                metadata=document.metadata,
            )
            for document in documents
        )