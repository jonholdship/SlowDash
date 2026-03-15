from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from fastapi import HTTPException, status

from dash_backend.config import ApiConfig


def _get_config() -> ApiConfig:
    return ApiConfig()


def create_access_token(
    payload: Dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT containing the given payload.

    The payload is shallow-copied so we can safely inject standard claims.
    """
    config = _get_config()
    to_encode = payload.copy()

    now = datetime.now(timezone.utc)
    if expires_delta is None:
        expires_delta = timedelta(hours=config.jwt_expires_hours)

    expire = now + expires_delta
    to_encode.update({"iat": int(now.timestamp()), "exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(
        to_encode,
        config.jwt_secret,
        algorithm=config.jwt_algorithm,
    )
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify a JWT and return its decoded payload.

    Raises HTTPException with 401 on failure so it can be used directly
    inside FastAPI dependencies.
    """
    config = _get_config()
    try:
        payload = jwt.decode(
            token,
            config.jwt_secret,
            algorithms=[config.jwt_algorithm],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

