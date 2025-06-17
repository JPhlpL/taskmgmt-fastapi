# src/schemas/task_schema.py
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class TaskSchema(BaseModel):
    email: EmailStr
    details: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CreateTaskRequest(BaseModel):
    email: EmailStr
    details: str
