# src/utils/auth.py
from fastapi import Header, HTTPException
from src.core.config import get_api_key


def verify_auth_token(x_auth_token: str = Header(...)) -> bool:
    expected_token = get_api_key()
    if x_auth_token != expected_token:
        raise HTTPException(status_code=403, detail="Invalid X_AUTH_API_KEY")
    return True
