from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.responses import JSONResponse
from typing import List

from src.schemas.schemas import CreateTaskRequest, TaskSchema, ChatRequest
from src.services.taskService import TaskService
from src.services.aiService import AIService
from src.utils.auth import verify_jwt_token, require_scopes

router = APIRouter(
    prefix="/tasks",
    dependencies=[Security(verify_jwt_token)],  # applies to all ops
    tags=["tasks"],
    # OR per-operation: use `Security(...)` in your decorator
)
service = TaskService()
ai_service = AIService()


@router.post(
    "/",
    response_model=TaskSchema,
    dependencies=[Depends(require_scopes(["tasks:create"]))],
)
async def create_task(
    payload: CreateTaskRequest,
):
    # You can also get the full claims via: claims = await Depends(verify_jwt_token)
    return await service.create_task(payload)


@router.get(
    "/",
    response_model=List[TaskSchema],
    dependencies=[Depends(require_scopes(["tasks:read"]))],
)
async def get_tasks(email: str):
    return await service.get_tasks_by_email(email)


@router.put(
    "/{id}",
    response_model=TaskSchema,
    dependencies=[Depends(require_scopes(["tasks:update"]))],
)
async def update_task(id: str, payload: CreateTaskRequest):
    return await service.update_task(id, payload.details)


@router.delete("/{id}", dependencies=[Depends(require_scopes(["tasks:delete"]))])
async def delete_task(id: str):
    return await service.delete_task(id)


@router.post(
    "/chat",
    summary="chat with bot",
    dependencies=[Depends(require_scopes(["tasks:create"]))],
)
async def chat_openai(request: ChatRequest):
    result = await service.generate_chat(request.prompt)
    return JSONResponse(content={"response": result})
