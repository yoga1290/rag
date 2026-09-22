import os

from yoga1290.rag.domain.ports import LLM
from yoga1290.rag.infrastructure.local.llm import (
    LlamaCppLLM,
)


class LLMFactory:

    @staticmethod
    def createLocalLlamaCppLLM() -> LLM:

        model_path = os.getenv(
            "LLAMACPP_MODEL_PATH",
            "./Mistral-7B-Instruct-v0.3.Q2_K.gguf",
        )

        temperature = float(
            os.getenv("LLAMACPP_TEMPERATURE", "0.15")
        )

        max_tokens = int(
            os.getenv("LLAMACPP_MAX_TOKENS", "450")
        )

        context_size = int(
            # os.getenv("LLAMACPP_CONTEXT", "4096")
            os.getenv("LLAMACPP_CONTEXT", "1096")
        )

        batch_size = int(
            os.getenv("LLAMACPP_BATCH", "384")
        )

        return LlamaCppLLM(
            model_path=model_path,
            temperature=temperature,
            max_tokens=max_tokens,
            context_size=context_size,
            batch_size=batch_size,
        )


    @staticmethod
    def create() -> LLM:
        #TODO
        return createLocalLlamaCppLLM()
