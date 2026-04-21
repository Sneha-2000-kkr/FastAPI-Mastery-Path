from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-12"
    version: str = "0.12.0"
    idempotency_ttl_seconds: int = 600


@lru_cache
def get_settings() -> Settings:
    return Settings()
