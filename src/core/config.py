# src/core/config.py
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")


def get_api_key():
    return os.getenv("X_AUTH_API_KEY")
