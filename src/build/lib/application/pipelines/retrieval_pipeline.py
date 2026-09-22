from yoga1290.rag.domain.models.rag_result import (
    RagResult,
    Source,
)
from yoga1290.rag.domain.ports import (
                                    LLM,
                                    Retriever, )


class RetrievalPipeline:

    def __init__(
        self,
        llm: LLM,
        retriever: Retriever,
        top_k: int = 2,
    ) -> None:
        self._llm = llm
        self._retriever = retriever
        self._top_k = top_k

    def run(self, question: str) -> RagResult:

        import time

        start = time.perf_counter()

        chunks = self._retriever.retrieve(
            question,
            top_k=self._top_k,
        )

        context = self._build_context(chunks)

        prompt = self._build_prompt(
            question=question,
            context=context,
        )

        answer = self._llm.generate(prompt)

        duration = time.perf_counter() - start

        sources = tuple(
            Source(
                document_id=chunk.document_id,
                chunk_id=chunk.id,
                metadata=chunk.metadata,
            )
            for chunk in chunks
        )

        return RagResult(
            question=question,
            answer=answer,
            sources=sources,
            duration_seconds=duration,
        )

    @staticmethod
    def _build_context(chunks) -> str:

        return "\n\n".join(
            chunk.text
            for chunk in chunks
        )

    @staticmethod
    def _build_prompt(
        question: str,
        context: str,
    ) -> str:

        return f"""
Use the following context to answer the question.

Context:
{context}

Question:
{question}

Answer:
""".strip()