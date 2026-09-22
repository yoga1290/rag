from yoga1290.rag.domain.ports.embedder import Embedder

class GTEEmbedder(Embedder):
    @property
    def dimension(self) -> int:
        raise NotImplementedError

    def embed(self, text: str) -> list[float]:
        raise NotImplementedError

    def embed_batch(self, texts):
        raise NotImplementedError
