from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-09"
    version: str = "0.9.0"
    cpu_workers: int = 2


@lru_cache
def get_settings() -> Settings:
    return Settings()
