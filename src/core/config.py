# src/core/config.py
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env.local")


def get_api_key():
    return os.getenv("X_AUTH_API_KEY")


def get_openai_key():
    return os.getenv("OPENAI_API_KEY")


def get_openai_admin_key():
    return os.getenv("OPENAI_API_ADMIN_KEY")
