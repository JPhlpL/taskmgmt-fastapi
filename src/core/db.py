# src/core/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in .env.local")

client = AsyncIOMotorClient(MONGO_URI)
db = client["taskmgmt"]
