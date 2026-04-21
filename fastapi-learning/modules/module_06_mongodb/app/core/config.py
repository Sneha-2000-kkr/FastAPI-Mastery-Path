from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-06"
    version: str = "0.6.0"
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "fapi"


@lru_cache
def get_settings() -> Settings:
    return Settings()
