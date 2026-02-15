from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
import json
import logging
from typing import Annotated
from urllib.parse import unquote

from dash_backend.strava.strava_client import get_athlete_id
from dash_backend.models import AuthenticatedUser, TokenResponse

app = FastAPI()
logger = logging.getLogger("uvicorn")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def _extract_access_token(token_param: str) -> TokenResponse:
    """Accept either a raw token string or a JSON serialized AccessInfo object and
    return the access token string to use with stravalib.
    """
    token_str = unquote(token_param)
    logger.info(f"Extracting access token from: {token_str}")
    token_dict = json.loads(token_str)
    parsed = TokenResponse.model_validate(token_dict)
    return parsed


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AuthenticatedUser:
    try:
        token_details = _extract_access_token(token)
        athlete_id = get_athlete_id(token_details)
    except:
        raise HTTPException(
            status_code=401, detail="Authentication failed, redirecting to login"
        )
    user = AuthenticatedUser(
        access_token=token_details.access_token,
        refresh_token=token_details.refresh_token,
        expires_at=token_details.expires_at,
        athlete_id=athlete_id,
    )
    return user
