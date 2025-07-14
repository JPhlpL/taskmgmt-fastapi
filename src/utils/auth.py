# src/utils/auth.py

import os
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

# ── CONFIG ─────────────────────────────────────────────────────────────────────

# Calculate project root (two levels up from this file: src/utils -> src -> App)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PEM_PATH = os.getenv(
    "CLERK_PUBLIC_KEY_PATH", os.path.join(ROOT_DIR, "scripts", "clerk_rsa_public.pem")
)

ISSUER = "https://smooth-gobbler-4.clerk.accounts.dev"

# ── LOAD PEM ───────────────────────────────────────────────────────────────────

if not os.path.exists(PEM_PATH):
    raise RuntimeError(f"Clerk public key not found at {PEM_PATH}")

with open(PEM_PATH, "r") as key_file:
    RSA_PUBLIC_KEY = key_file.read()

# ── SECURITY DEPENDENCY ─────────────────────────────────────────────────────────

bearer_scheme = HTTPBearer()


def verify_jwt_token(
    creds: HTTPAuthorizationCredentials = Security(bearer_scheme),
) -> dict:
    """
    1. Reads Authorization: Bearer <token>
    2. Verifies RS256 signature against local PEM, checks `iss` and `exp`
    3. Returns decoded payload (custom + standard claims)
    """
    token = creds.credentials
    try:
        payload = jwt.decode(
            token,
            RSA_PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={"verify_aud": False},  # set audience if you need it
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid or expired JWT token")

    return payload


def require_scopes(required_scopes: list[str]):
    """
    Returns a dependency that ensures payload['scopes'] includes all required_scopes.
    Raises HTTPException(403) if any are missing.
    """

    def dependency(claims: dict = Depends(verify_jwt_token)):
        token_scopes = claims.get("scopes", [])
        missing = [s for s in required_scopes if s not in token_scopes]
        if missing:
            raise HTTPException(
                status_code=403, detail=f"Missing required scopes: {missing}"
            )
        return claims

    return dependency
