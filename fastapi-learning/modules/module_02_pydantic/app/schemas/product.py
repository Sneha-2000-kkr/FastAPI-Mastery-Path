from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import Field

from app.schemas.common import CamelModel


class _ProductBase(CamelModel):
    id: int
    name: str = Field(min_length=1, max_length=200)
    price_cents: int = Field(ge=0)


class Book(_ProductBase):
    kind: Literal["book"] = "book"
    author: str
    pages: int = Field(gt=0)


class Electronic(_ProductBase):
    kind: Literal["electronic"] = "electronic"
    warranty_months: int = Field(ge=0, le=120)
    voltage: int = Field(ge=1, le=480)


Product = Annotated[Union[Book, Electronic], Field(discriminator="kind")]


class BookCreate(CamelModel):
    kind: Literal["book"] = "book"
    name: str
    price_cents: int = Field(ge=0)
    author: str
    pages: int = Field(gt=0)


class ElectronicCreate(CamelModel):
    kind: Literal["electronic"] = "electronic"
    name: str
    price_cents: int = Field(ge=0)
    warranty_months: int = Field(ge=0, le=120)
    voltage: int = Field(ge=1, le=480)


ProductCreate = Annotated[Union[BookCreate, ElectronicCreate], Field(discriminator="kind")]
