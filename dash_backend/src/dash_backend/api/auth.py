from typing import Annotated

from fastapi import Cookie, Depends, HTTPException, status

from dash_backend.auth_jwt import verify_token
from dash_backend.models import AuthenticatedUser


async def get_current_user(
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

    payload = verify_token(auth_token)

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

    return user
