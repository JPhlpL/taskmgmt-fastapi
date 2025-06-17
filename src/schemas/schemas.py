from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID


class TaskSchema(BaseModel):
    id: UUID
    email: EmailStr
    details: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateTaskRequest(BaseModel):
    email: EmailStr
    details: str
