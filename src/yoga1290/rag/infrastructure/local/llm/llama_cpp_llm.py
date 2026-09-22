from yoga1290.rag.domain.ports.llm import LLM

from pydantic import BaseModel


class LlamaCppLLM(LLM):

    def __init__(
        self,
        model_path: str,
        temperature: float = 0.15,
        max_tokens: int = 450,
        context_size: int = 4096,
        batch_size: int = 384,
    ) -> None:
        from langchain_community.llms import LlamaCpp
        self._llm = LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            n_ctx=context_size,
            n_batch=batch_size,
            verbose=False,
        )

    def generate(self, prompt: str) -> str:
        return self._llm.invoke(prompt)

    def with_structured_output(self,
                        schema: BaseModel): #TODO
        return self._llm.with_structured_output(schema)