from pydantic import BaseModel, EmailStr


class EmailIn(BaseModel):
    user_id: int
    to: EmailStr
    subject: str
    body: str


class ReportIn(BaseModel):
    user_id: int


class EnqueueOut(BaseModel):
    task_id: str
    queue: str
