from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")

    app_name: str = "fastapi-learning-module-05"
    version: str = "0.5.0"
    database_url: str = "postgresql+asyncpg://fapi:fapi@localhost:5432/fapi"
    db_echo: bool = False
    db_pool_size: int = 10
    db_max_overflow: int = 20


@lru_cache
def get_settings() -> Settings:
    return Settings()
