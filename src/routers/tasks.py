# src/routers/task_router.py
from fastapi import APIRouter, Depends, Header, HTTPException
from src.schemas.schemas import CreateTaskRequest, TaskSchema
from src.services.taskService import TaskService
from src.utils.auth import verify_auth_token
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])
service = TaskService()


@router.get("/health-check")
async def health_check_endpoint() -> JSONResponse:
    return JSONResponse({"status": "working!"})


@router.post("/", response_model=TaskSchema)
async def create_task(payload: CreateTaskRequest, _: bool = Depends(verify_auth_token)):
    return await service.create_task(payload)


@router.get("/", response_model=List[TaskSchema])
async def get_tasks(email: str, _: bool = Depends(verify_auth_token)):
    return await service.get_tasks_by_email(email)


@router.put("/{id}", response_model=TaskSchema)
async def update_task(
    id: str, payload: CreateTaskRequest, _: bool = Depends(verify_auth_token)
):
    return await service.update_task(id, payload.details)


@router.delete("/{id}")
async def delete_task(id: str, _: bool = Depends(verify_auth_token)):
    return await service.delete_task(id)
