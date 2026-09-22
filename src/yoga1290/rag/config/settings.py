from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_env: str = "local"
    ai_provider: str = "local"
    parser_provider: str = "docling"
    extractor_provider: str = "qwen"
    classifier_provider: str = "qwen"
    search_preparer_provider: str = "local"
    embedding_provider: str = "qwen"
    vector_store_provider: str = "pgvector"
