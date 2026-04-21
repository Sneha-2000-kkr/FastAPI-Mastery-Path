"""Standard envelope helpers for consistent API responses across modules."""
from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Envelope(BaseModel, Generic[T]):
    """Uniform success envelope: {data, meta}."""
    data: T
    meta: Optional[dict[str, Any]] = None


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Optional[dict[str, Any]] = None


class ErrorEnvelope(BaseModel):
    error: ErrorBody


def ok(data: Any, meta: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return {"data": data, "meta": meta}


def err(code: str, message: str, details: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    return {"error": {"code": code, "message": message, "details": details}}
