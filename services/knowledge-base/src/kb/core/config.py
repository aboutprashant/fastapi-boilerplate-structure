from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Knowledge Base"
    environment: Literal["local", "test", "staging", "production"] = "local"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    jwt_secret: str = "local-secret"
    database_url: str = "sqlite+aiosqlite:///./.local/knowledge_base.db"
    redis_url: str = "redis://localhost:6379/0"
    use_mock_embeddings: bool = True
    use_mock_answer_generator: bool = True
    use_mock_vector_search: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
