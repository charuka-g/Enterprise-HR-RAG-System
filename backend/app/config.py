from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_db_url: str             # required — PostgreSQL connection string
    openai_api_key: str              # required — loaded from OPENAI_API_KEY env var
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536
    openai_model: str = "gpt-4o"
    top_k_retrieve: int = 20         # candidates from vector search
    top_k_prompt: int = 5            # chunks sent in the prompt
    max_tokens: int = 2048
    log_file: str = "logs/queries.jsonl"
    cors_origins_str: str = "http://localhost:5173,http://localhost:3000"

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins_str.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
