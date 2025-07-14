from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/tasks", tags=["debug"])


@router.get("/health-check")
async def health_check_endpoint() -> JSONResponse:
    return JSONResponse({"status": "working!"})
