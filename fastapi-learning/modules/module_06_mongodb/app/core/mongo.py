from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

_client: AsyncIOMotorClient | None = None


def init_client() -> AsyncIOMotorClient:
    global _client
    s = get_settings()
    _client = AsyncIOMotorClient(s.mongo_url, uuidRepresentation="standard")
    return _client


def close_client() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_db() -> AsyncIOMotorDatabase:
    if _client is None:
        raise RuntimeError("Mongo client not initialised — call init_client() in lifespan")
    return _client[get_settings().mongo_db]
