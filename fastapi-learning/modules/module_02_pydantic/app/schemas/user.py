from __future__ import annotations

import re
from typing import Optional

from pydantic import EmailStr, Field, computed_field, field_validator

from app.schemas.common import CamelModel

_PASSWORD_RE = re.compile(r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{10,}$")


class UserCreate(CamelModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128, repr=False)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)

    @field_validator("password")
    @classmethod
    def _strong(cls, v: str) -> str:
        if not _PASSWORD_RE.match(v):
            raise ValueError(
                "password must be ≥10 chars and include an uppercase letter, a digit, and a symbol"
            )
        return v


class UserRead(CamelModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str

    @computed_field  # type: ignore[misc]
    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class UserUpdate(CamelModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=80)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=80)
