from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=120)


class CustomerRead(BaseModel):
    id: int
    email: EmailStr
    name: str
