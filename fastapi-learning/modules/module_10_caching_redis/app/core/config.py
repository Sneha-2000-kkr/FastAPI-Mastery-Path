from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-10"
    version: str = "0.10.0"
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl_seconds: int = 60
    cache_namespace: str = "fapi"


@lru_cache
def get_settings() -> Settings:
    return Settings()
