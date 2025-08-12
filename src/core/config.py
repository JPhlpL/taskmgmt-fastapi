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


def get_taskmgmt_username_doc():
    return os.getenv("TASKMGMT_USERNAME_DOC")


def get_taskmgmt_password_doc():
    return os.getenv("TASKMGMT_PASSWORD_DOC")
