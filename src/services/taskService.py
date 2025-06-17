# src/services/task_service.py
from src.repositories.taskRepository import TaskRepository
from src.schemas.schemas import CreateTaskRequest, TaskSchema
from src.core.logger import setup_logger

logger = setup_logger()


class TaskService:
    def __init__(self):
        self.repo = TaskRepository()

    async def create_task(self, payload: CreateTaskRequest) -> TaskSchema:
        logger.info(f"Creating task for: {payload.email}")
        task = await self.repo.create_task(email=payload.email, details=payload.details)
        return TaskSchema(**task)
