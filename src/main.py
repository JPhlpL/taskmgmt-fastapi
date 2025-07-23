# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import tasks, debug
from src.core.logger import setup_logger

web_app = FastAPI()
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
