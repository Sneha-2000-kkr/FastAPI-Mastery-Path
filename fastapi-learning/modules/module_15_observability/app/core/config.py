from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-15"
    version: str = "0.15.0"
    enable_tracing: bool = False  # flip on once OTel deps installed
    otlp_endpoint: str = "http://localhost:4318/v1/traces"


@lru_cache
def get_settings() -> Settings:
    return Settings()
