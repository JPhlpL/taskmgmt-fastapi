# src/routers/task_router.py
from fastapi import APIRouter, Depends, Header, HTTPException
from src.schemas.schemas import CreateTaskRequest, TaskSchema
from src.services.taskService import TaskService
from src.utils.auth import verify_auth_token

router = APIRouter(prefix="/tasks", tags=["Tasks"])
service = TaskService()


@router.post("/", response_model=TaskSchema)
async def create_task(payload: CreateTaskRequest, _: bool = Depends(verify_auth_token)):
    return await service.create_task(payload)
