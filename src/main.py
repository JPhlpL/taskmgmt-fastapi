# main.py
import secrets
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

from src.routers import tasks, debug, ai
from src.core.logger import setup_logger
from src.core.config import get_taskmgmt_username_doc, get_taskmgmt_password_doc

web_app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
setup_logger()

web_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_app.include_router(tasks.router)
web_app.include_router(debug.router)
web_app.include_router(ai.router)

security = HTTPBasic()


def get_current_username(
    credentials: HTTPBasicCredentials = Depends(security),
) -> str:
    correct_username = secrets.compare_digest(
        credentials.username, get_taskmgmt_username_doc()
    )
    correct_password = secrets.compare_digest(
        credentials.password, get_taskmgmt_password_doc()
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


# Re-expose /docs behind Basic auth
@web_app.get("/docs", include_in_schema=False)
def custom_swagger_ui(
    username: str = Depends(get_current_username),
):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Taskmgmt API Docs")


# Re-expose /redoc behind Basic auth
@web_app.get("/redoc", include_in_schema=False)
def custom_redoc_ui(
    username: str = Depends(get_current_username),
):
    return get_redoc_html(openapi_url="/openapi.json", title="Tasmgmt API ReDoc")


# Re-expose /openapi.json behind Basic auth
@web_app.get("/openapi.json", include_in_schema=False)
def custom_openapi(
    username: str = Depends(get_current_username),
):
    return get_openapi(
        title=web_app.title,
        version=web_app.version,
        routes=web_app.routes,
    )
