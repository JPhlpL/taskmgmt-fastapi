import uuid
from typing import List
from bson import ObjectId
from src.models.models import TaskModel
from src.core.db import db
from datetime import datetime


class TaskRepository:
    def __init__(self):
        self.collection = db["tasks"]

    async def create_task(self, email: str, details: str) -> TaskModel:
        now = datetime.utcnow()
        task: TaskModel = {
            "id": str(uuid.uuid4()),
            "email": email,
            "details": details,
            "created_at": now,
            "updated_at": now,
        }
        await self.collection.insert_one(task)
        return task

    async def get_tasks_by_email(self, email: str) -> List[TaskModel]:
        tasks = await self.collection.find({"email": email}).to_list(length=None)
        return tasks

    async def update_task(self, id: str, details: str) -> TaskModel | None:
        result = await self.collection.find_one_and_update(
            {"id": id},
            {"$set": {"details": details, "updated_at": datetime.utcnow()}},
            return_document=True,
        )
        return result

    async def delete_task(self, id: str) -> bool:
        result = await self.collection.delete_one({"id": id})
        return result.deleted_count == 1
