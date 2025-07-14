import os
import json
import requests
from functools import lru_cache
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from jose.utils import base64url_decode
from typing import Dict, List

# ── CONFIG ─────────────────────────────────────────────────────────────────────

# Local PEM fallback
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
PEM_PATH = os.path.join(ROOT_DIR, "scripts", "clerk_rsa_public.pem")

# Clerk issuer & JWKS endpoint
ISSUER = "https://smooth-gobbler-4.clerk.accounts.dev"
JWKS_URL = ISSUER + "/.well-known/jwks.json"

# HTTP Bearer scheme
bearer = HTTPBearer()

# ── UTILITIES ──────────────────────────────────────────────────────────────────


@lru_cache()  # cache the JWKS for the lifetime of the process
def get_jwks() -> Dict:
    """Fetch and cache Clerk’s JWKS."""
    resp = requests.get(JWKS_URL, timeout=5)
    if not resp.ok:
        raise HTTPException(503, "Cannot fetch JWKS from Clerk")
    return resp.json()


def get_signing_key(token: str):
    """
    Extracts `kid` from token header, finds matching JWK and
    returns a PEM-formatted public key.
    """
    header = jwt.get_unverified_header(token)
    jwks = get_jwks().get("keys", [])
    for jwk in jwks:
        if jwk["kid"] == header.get("kid"):
            # jose expects the JWK dict as JSON string
            return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    # Fallback: try static PEM if JWKS lookup fails
    if os.path.exists(PEM_PATH):
        return open(PEM_PATH).read()
    raise HTTPException(401, "Invalid token `kid` – no matching JWK or PEM")


# ── DEPENDENCIES ────────────────────────────────────────────────────────────────


def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
) -> Dict:
    """
    1. Reads `Authorization: Bearer <token>`
    2. Fetches signing key (JWKS or local PEM)
    3. Verifies RS256 signature, `iss`, `exp`
    4. Returns the decoded payload (custom + standard claims)
    """
    token = credentials.credentials
    try:
        key = get_signing_key(token)
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={"verify_aud": False},  # set `audience=` + True if you use `aud`
        )
    except JWTError:
        raise HTTPException(401, "Invalid or expired JWT token")

    return payload


def require_scopes(required: List[str]):
    """
    Dependency factory: ensures `payload["scopes"]` includes all `required`.
    Raises 403 if any are missing.
    """

    def dependency(claims: Dict = Depends(verify_jwt_token)):
        scopes = claims.get("scopes", [])
        missing = [s for s in required if s not in scopes]
        if missing:
            raise HTTPException(403, f"Missing required scopes: {missing}")
        return claims

    return dependency
