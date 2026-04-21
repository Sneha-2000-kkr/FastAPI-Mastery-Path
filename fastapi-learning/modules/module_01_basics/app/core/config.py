from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")

    app_name: str = "fastapi-learning-module-01"
    debug: bool = False
    version: str = "0.1.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
