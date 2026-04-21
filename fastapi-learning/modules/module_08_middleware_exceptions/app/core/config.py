from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-08"
    version: str = "0.8.0"
    max_body_bytes: int = 1 * 1024 * 1024  # 1 MB


@lru_cache
def get_settings() -> Settings:
    return Settings()
