# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import tasks, debug
from src.core.logger import setup_logger

app = FastAPI()
setup_logger()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router)
app.include_router(debug.router)
