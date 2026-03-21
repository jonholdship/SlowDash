import time
from datetime import datetime, timedelta, timezone
from fastapi import Cookie, Response, HTTPException, status
import jwt
from typing import Annotated, Any

from dash_backend.config import ApiConfig
from dash_backend.models import AuthenticatedUser
from dash_backend.strava.strava_client import refresh_strava_tokens

# Refresh Strava access token this many seconds before it expires.
_STRAVA_REFRESH_BUFFER_SEC = 600



def create_access_token(
    payload: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT containing the given payload.

    The payload is shallow-copied so we can safely inject standard claims.
    """
    config = ApiConfig()
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


def _verify_token(token: str) -> dict[str, Any]:
    """
    Verify a JWT and return its decoded payload.

    Raises HTTPException with 401 on failure so it can be used directly
    inside FastAPI dependencies.
    """
    config = ApiConfig()
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



def set_auth_cookie(response: Response, user: AuthenticatedUser):
    # Issue JWT and set it as an httpOnly cookie
    config = ApiConfig()
    jwt_payload = {
        "access_token": user.access_token,
        "refresh_token": user.refresh_token,
        "expires_at": user.expires_at,
        "athlete_id": user.athlete_id,
    }
    jwt_token = create_access_token(jwt_payload)
    max_age = int(timedelta(hours=config.jwt_expires_hours).total_seconds())

    # Note: in production, set secure=True and tune samesite
    response.set_cookie(
        key="auth_token",
        value=jwt_token,
        httponly=True,
        samesite="lax",
        max_age=max_age,
    )
    return response


def clear_auth_cookie(response: Response) -> None:
    response.delete_cookie(key="auth_token", httponly=True, samesite="lax")


def _strava_access_needs_refresh(expires_at: int, now: int) -> bool:
    return now >= expires_at - _STRAVA_REFRESH_BUFFER_SEC


async def get_current_user(
    response: Response,
    auth_token: Annotated[str | None, Cookie(alias="auth_token")] = None,
) -> AuthenticatedUser:
    """
    Resolve the current user from a JWT stored in an httpOnly cookie.
    """
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    payload = _verify_token(auth_token)

    try:
        user = AuthenticatedUser(
            access_token=payload["access_token"],
            refresh_token=payload.get("refresh_token", ""),
            expires_at=payload["expires_at"],
            athlete_id=payload["athlete_id"],
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token payload",
        )

    now = int(time.time())
    if _strava_access_needs_refresh(user.expires_at, now):
        if not user.refresh_token:
            clear_auth_cookie(response)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        try:
            user = refresh_strava_tokens(user)
        except Exception:
            clear_auth_cookie(response)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired, please sign in again",
            )
        set_auth_cookie(response, user)

    return user
