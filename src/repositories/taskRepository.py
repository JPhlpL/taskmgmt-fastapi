# src/repositories/task_repository.py
from datetime import datetime
from src.core.db import db
from src.models.models import TaskModel


class TaskRepository:
    def __init__(self):
        self.collection = db["tasks"]

    async def create_task(self, email: str, details: str) -> TaskModel:
        now = datetime.utcnow()
        task: TaskModel = {
            "email": email,
            "details": details,
            "created_at": now,
            "updated_at": now,
        }
        await self.collection.insert_one(task)
        return task
