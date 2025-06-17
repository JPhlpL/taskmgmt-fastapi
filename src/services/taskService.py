# src/services/task_service.py
from src.repositories.taskRepository import TaskRepository
from src.schemas.schemas import CreateTaskRequest, TaskSchema
from src.core.logger import setup_logger
from typing import List
from fastapi import HTTPException

logger = setup_logger()


class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    async def create_task(self, payload: CreateTaskRequest) -> TaskSchema:
        logger.info(f"Creating task for: {payload.email}")
        task = await self.repo.create_task(email=payload.email, details=payload.details)
        return TaskSchema(**task)

    async def get_tasks_by_email(self, email: str) -> List[TaskSchema]:
        tasks = await self.repo.get_tasks_by_email(email)
        return [TaskSchema(**task) for task in tasks]

    async def update_task(self, id: str, details: str) -> TaskSchema:
        updated = await self.repo.update_task(id, details)
        if not updated:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskSchema(**updated)

    async def delete_task(self, id: str) -> dict:
        success = await self.repo.delete_task(id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": f"Task {id} deleted successfully"}
