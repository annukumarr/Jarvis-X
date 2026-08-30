"""
api/auth.py

Purpose:
Owner authentication for JARVIS-X.

This module:
- Authenticates the JARVIS-X owner.
- Creates a signed authentication token.
- Stores the token in an HTTP-only cookie.
- Verifies the owner session.
- Provides logout functionality.

No database is used for authentication at this stage.
"""

import base64
import hashlib
import hmac
import json
import os
import time

from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, HTTPException, Response
from pydantic import BaseModel


# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv()

OWNER_PASSWORD = os.getenv("JARVIS_OWNER_PASSWORD")
AUTH_SECRET = os.getenv("JARVIS_AUTH_SECRET")

if not OWNER_PASSWORD:
    raise RuntimeError(
        "JARVIS_OWNER_PASSWORD is missing from .env"
    )

if not AUTH_SECRET:
    raise RuntimeError(
        "JARVIS_AUTH_SECRET is missing from .env"
    )


# ==========================================================
# SETTINGS
# ==========================================================

AUTH_COOKIE_NAME = "jarvis_owner_token"

TOKEN_EXPIRATION_SECONDS = 60 * 60 * 24
# 24 hours


# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


# ==========================================================
# REQUEST MODEL
# ==========================================================

class LoginRequest(BaseModel):
    password: str


# ==========================================================
# TOKEN HELPERS
# ==========================================================

def _create_token() -> str:
    """
    Create a signed owner authentication token.
    """

    payload = {
        "role": "owner",
        "iat": int(time.time()),
        "exp": int(time.time()) + TOKEN_EXPIRATION_SECONDS,
    }

    payload_json = json.dumps(
        payload,
        separators=(",", ":"),
    ).encode("utf-8")

    payload_encoded = base64.urlsafe_b64encode(
        payload_json
    ).decode("utf-8").rstrip("=")

    signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        payload_encoded.encode("utf-8"),
        hashlib.sha256,
    ).digest()

    signature_encoded = base64.urlsafe_b64encode(
        signature
    ).decode("utf-8").rstrip("=")

    return f"{payload_encoded}.{signature_encoded}"


def _verify_token(token: str) -> bool:
    """
    Verify token signature and expiration.
    """

    try:
        payload_encoded, signature_encoded = token.split(".", 1)

        expected_signature = hmac.new(
            AUTH_SECRET.encode("utf-8"),
            payload_encoded.encode("utf-8"),
            hashlib.sha256,
        ).digest()

        expected_signature_encoded = (
            base64.urlsafe_b64encode(
                expected_signature
            )
            .decode("utf-8")
            .rstrip("=")
        )

        if not hmac.compare_digest(
            signature_encoded,
            expected_signature_encoded,
        ):
            return False

        padding = "=" * (
            -len(payload_encoded) % 4
        )

        payload_json = base64.urlsafe_b64decode(
            payload_encoded + padding
        )

        payload = json.loads(
            payload_json.decode("utf-8")
        )

        if payload.get("role") != "owner":
            return False

        if int(payload.get("exp", 0)) < int(time.time()):
            return False

        return True

    except Exception:
        return False


# ==========================================================
# LOGIN
# ==========================================================

@router.post("/login")
def login(
    request: LoginRequest,
    response: Response,
):
    """
    Authenticate the JARVIS-X owner.
    """

    if not hmac.compare_digest(
        request.password,
        OWNER_PASSWORD,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid owner password.",
        )

    token = _create_token()

    response.set_cookie(
        key=AUTH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=TOKEN_EXPIRATION_SECONDS,
    )

    return {
        "success": True,
        "authenticated": True,
        "role": "owner",
        "message": "Owner authentication successful.",
    }


# ==========================================================
# CURRENT SESSION
# ==========================================================

@router.get("/me")
def current_user(
    jarvis_owner_token: str | None = Cookie(default=None),
):
    """
    Check the current JARVIS-X authentication session.
    """

    if not jarvis_owner_token:
        return {
            "success": True,
            "authenticated": False,
            "role": "user",
        }

    if not _verify_token(jarvis_owner_token):
        return {
            "success": True,
            "authenticated": False,
            "role": "user",
        }

    return {
        "success": True,
        "authenticated": True,
        "role": "owner",
    }


# ==========================================================
# LOGOUT
# ==========================================================

@router.post("/logout")
def logout(response: Response):
    """
    End the owner authentication session.
    """

    response.delete_cookie(
        key=AUTH_COOKIE_NAME,
    )

    return {
        "success": True,
        "authenticated": False,
        "role": "user",
        "message": "Owner session ended.",
    }


# ==========================================================
# OWNER CHECK
# ==========================================================

def is_owner(
    jarvis_owner_token: str | None,
) -> bool:
    """
    Internal helper used by protected JARVIS-X endpoints.
    """

    if not jarvis_owner_token:
        return False

    return _verify_token(
        jarvis_owner_token
    )