from datetime import datetime
from typing import Annotated, Any, Optional

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, BeforeValidator, ConfigDict, Field


def _validate_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str):
        try:
            ObjectId(v)
        except InvalidId as exc:
            raise ValueError("invalid ObjectId") from exc
        return v
    raise TypeError("ObjectId or str required")


PyObjectId = Annotated[str, BeforeValidator(_validate_object_id)]


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=120)


class ArticleRead(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: PyObjectId = Field(alias="_id")
    title: str
    body: str
    author: str
    created_at: datetime


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    body: Optional[str] = Field(default=None, min_length=1)
