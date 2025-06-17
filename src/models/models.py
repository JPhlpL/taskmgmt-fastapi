# src/models/task_model.py
from datetime import datetime
from typing import TypedDict


class TaskModel(TypedDict):
    email: str
    details: str
    created_at: datetime
    updated_at: datetime
