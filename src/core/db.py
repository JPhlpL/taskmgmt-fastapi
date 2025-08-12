# src/core/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import get_mongo_uri


client = AsyncIOMotorClient(get_mongo_uri())
db = client["taskmgmt"]
