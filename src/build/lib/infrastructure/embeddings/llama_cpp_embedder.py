from yoga1290.rag.domain.ports.embedder import Embedder

import os

class LlamaCppEmbeddings(Embedder):
    from llama_cpp import Llama
    from langchain_core.embeddings import Embeddings

    def __init__(self,
        LLAMACPP_EMBEDDING_MODEL_PATH =os.getenv('LLAMACPP_EMBEDDING_MODEL_PATH', './Qwen3-Embedding-0.6B-Q8_0.gguf'),
        LLAMACPP_EMBEDDING_CONTEXT:int =int(os.getenv('LLAMACPP_EMBEDDING_CONTEXT', '768')),
        LLAMACPP_EMBEDDING_N_BATCH:int =int(os.getenv('LLAMACPP_EMBEDDING_N_BATCH', '300')),
    ):
        self.llm_embed = self.DirectLlamaCppEmbeddings(
            model_path=LLAMACPP_EMBEDDING_MODEL_PATH,
            n_ctx=LLAMACPP_EMBEDDING_CONTEXT,
            n_batch=LLAMACPP_EMBEDDING_N_BATCH,
            # n_seq_max=1,  # allow up to 8 texts to be packed into one decode call
            embedding=True,
            n_threads=os.cpu_count(),
        )

    @property
    def dimension(self) -> int:
        raise NotImplementedError

    def embed(self, text: str) -> list[float]:
        return self.llm_embed.embed_documents(text)

    def embed_query(self, text: str) -> list[float]:
        return self.llm_embed.embed_query(text)

    def embed_documents(self, text: str) -> list[float]:
        return self.llm_embed.embed_documents(text)
    
    def embed_batch(self, texts):
        raise NotImplementedError

    class DirectLlamaCppEmbeddings(Embeddings):
        # custom implementation of langchain_community.embeddings.llamacpp.LlamaCppEmbeddings
        def __init__(self, model_path,
                    n_ctx=768,
                    n_batch=500,
                    n_seq_max=8,
                    embedding=True,
                    n_threads=None):

            from llama_cpp import Llama
            self._client = Llama(
                model_path=model_path,
                embedding=True,
                n_ctx=n_ctx,
                n_batch=n_batch,
                n_seq_max=n_seq_max,   # <-- the missing piece
                n_threads=n_threads or __import__('os').cpu_count(),
            )
    
        # def embed_documents(self, texts):
        #     return [e for e in self._client.create_embedding(texts)['data']]
    
        # def embed_query(self, text):
        #     return self.embed_documents([text])[0]
        def embed_documents(self, texts):
            return [self.embed_query(t) for t in texts]  # ✅ one call per text
        
        def embed_query(self, text):
            result = self._client.create_embedding(text)  # note: single string, not [text]
            # print(f'embed_query {result}')
            return result['data'][0]['embedding']


    
