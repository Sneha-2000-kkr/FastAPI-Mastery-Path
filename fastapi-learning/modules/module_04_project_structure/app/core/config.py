from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-04"
    version: str = "0.4.0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
