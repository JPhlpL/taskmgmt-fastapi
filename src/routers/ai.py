from fastapi import APIRouter, Depends, Security
from fastapi.responses import JSONResponse
from typing import List

from src.schemas.schemas import ChatRequest
from src.services.aiService import AIService
from src.utils.auth import verify_jwt_token, require_scopes

router = APIRouter(
    prefix="/ai",
    # dependencies=[Security(verify_jwt_token)],  # applies to all ops
    tags=["Artificial Intelligence"],
    # OR per-operation: use `Security(...)` in your decorator
)
ai_service = AIService()


@router.post(
    "/chat",
    summary="chat with bot",
    # dependencies=[Depends(require_scopes(["tasks:create"]))],
)
async def chat_openai(request: ChatRequest):
    result = await ai_service.generate_chat(request.prompt)
    return JSONResponse(content={"response": result})


@router.get("/balance", summary="Get OpenAI credit grants")
async def balance():
    data = await ai_service.get_balance()
    return JSONResponse(content=data)
