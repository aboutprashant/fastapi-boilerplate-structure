from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Assistant Gateway"
    environment: Literal["local", "test", "staging", "production"] = "local"
    log_level: str = "INFO"
    api_v1_prefix: str = "/api/v1"
    jwt_secret: str = "local-secret"
    knowledge_base_url: str = "http://localhost:8001"
    data_analytics_url: str = "http://localhost:8003"
    use_mock_llm: bool = True
    use_mock_service_clients: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
