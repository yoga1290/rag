from yoga1290.rag.domain.ports.vector_store import VectorStore

class DatabricksVectorStore(VectorStore):
    def upsert(self, chunks) -> None:
        raise NotImplementedError

    def delete(self, document_id: str) -> None:
        raise NotImplementedError

    def search(self, embedding, *, top_k=10, filters=None):
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError
