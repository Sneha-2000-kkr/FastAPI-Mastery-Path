from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class ArticleRepository:
    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.col = db["articles"]

    async def ensure_indexes(self) -> None:
        await self.col.create_index("author")
        await self.col.create_index([("created_at", -1)])

    async def list(self, *, limit: int, skip: int) -> list[dict[str, Any]]:
        cursor = self.col.find().sort("created_at", -1).skip(skip).limit(limit)
        return [doc async for doc in cursor]

    async def get(self, article_id: str) -> dict[str, Any] | None:
        return await self.col.find_one({"_id": ObjectId(article_id)})

    async def create(self, *, title: str, body: str, author: str) -> dict[str, Any]:
        doc = {
            "title": title,
            "body": body,
            "author": author,
            "created_at": datetime.now(timezone.utc),
        }
        res = await self.col.insert_one(doc)
        doc["_id"] = res.inserted_id
        return doc

    async def update(self, article_id: str, patch: dict[str, Any]) -> dict[str, Any] | None:
        if not patch:
            return await self.get(article_id)
        res = await self.col.find_one_and_update(
            {"_id": ObjectId(article_id)},
            {"$set": patch},
            return_document=True,
        )
        return res

    async def delete(self, article_id: str) -> bool:
        res = await self.col.delete_one({"_id": ObjectId(article_id)})
        return res.deleted_count == 1
