from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="APP_", extra="ignore")
    app_name: str = "fastapi-learning-module-07"
    version: str = "0.7.0"

    jwt_secret: str = "change-me"
    jwt_alg: str = "HS256"
    jwt_expires_min: int = 15
    jwt_issuer: str = "fapi-learning"
    jwt_audience: str = "fapi-learning-clients"


@lru_cache
def get_settings() -> Settings:
    return Settings()
