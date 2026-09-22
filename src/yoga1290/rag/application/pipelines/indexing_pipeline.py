from yoga1290.rag.domain.ports.embedder import Embedder
from yoga1290.rag.domain.ports.vector_store import VectorStore

class IndexingPipeline:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store

    def index(self, search_document):
        chunks = list(search_document.chunks)
        texts = [chunk.text for chunk in chunks]
        embeddings = self.embedder.embed_batch(texts)

        indexed_chunks = [
            chunk.__class__(
                id=chunk.id,
                document_id=chunk.document_id,
                text=chunk.text,
                index=chunk.index,
                embedding=embedding,
                metadata=chunk.metadata,
            )
            for chunk, embedding in zip(
                chunks,
                embeddings,
                strict=True,
            )
        ]

        self.vector_store.upsert(indexed_chunks)
