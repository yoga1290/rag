from yoga1290.rag.domain.ports.embedder import Embedder
from yoga1290.rag.domain.ports.vector_store import VectorStore

class SearchService:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: VectorStore,
    ) -> None:
        self.embedder = embedder
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        *,
        top_k: int = 10,
        filters: dict[str, object] | None = None,
    ):
        embedding = self.embedder.embed(query)
        return self.vector_store.search(
            embedding,
            top_k=top_k,
            filters=filters,
        )
