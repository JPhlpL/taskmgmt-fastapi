from datetime import datetime
from uuid import UUID
from typing import TypedDict


class TaskModel(TypedDict):
    id: UUID
    email: str
    details: str
    created_at: datetime
    updated_at: datetime
