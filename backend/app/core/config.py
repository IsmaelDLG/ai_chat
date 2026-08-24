from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI Chat API"
    environment: str = "development"

    llm_base_url: str = "http://127.0.0.1:11434/v1/"
    llm_api_key: str = "ollama"
    llm_model: str = "qwen2.5-coder:7b"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Store instance of `Settings` in a cache to avoid reloading it on each request.
    """
    return Settings()