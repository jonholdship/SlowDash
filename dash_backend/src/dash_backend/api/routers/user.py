import logging
from typing import Annotated

from fastapi import BackgroundTasks, Depends, Response, APIRouter 
from sqlalchemy.orm import Session

from dash_backend.api.auth import get_current_user, set_auth_cookie
from dash_backend.models import AuthenticatedUser, UserSettings
from dash_backend.strava.strava_client import athlete_login, get_activity_summaries
from dash_database.crud import (
    athlete_exists,
    get_athlete,
    get_latest_activity,
    update_athlete,
    write_activities,
    write_athlete,
    delete_activities,
)
from dash_database.schemas import User
from dash_database.session import SessionLocal

router = APIRouter(prefix="/user", tags=["user"])
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me")
def get_me(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
) -> dict:
    """
    Return minimal information about the currently authenticated user.
    """
    return {
        "athlete_id": user.athlete_id,
    }


def update_activities(user: AuthenticatedUser):
    """
    Update the database with any activities recorded since last log in.
    Uses its own DB session so it is safe to run in a background task.
    """
    session = SessionLocal()
    try:
        last_retrieved_date = None
        athlete = get_athlete(session, user.athlete_id)
        if athlete_exists(session, athlete.id):
            last_retrieved_date = get_latest_activity(session, athlete.id)
        else:
            athlete = User.model_validate(athlete.model_dump())
            athlete = write_athlete(session, athlete)
        if not last_retrieved_date:
            last_retrieved_date = athlete.start_date
        activities = get_activity_summaries(user=user, start_date=last_retrieved_date)
        write_activities(session, activities)
    finally:
        session.close()


@router.get("/login")
def user_login(
    access_code: str,
    response: Response,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db),
) -> bool:
    """
    Take short lived access code and exchange for token through Strava API.
    Update the database with any activities recorded since last log in.
    """
    logger.info("logging in with access code")
    athlete, user = athlete_login(access_code)
    if not athlete_exists(session, athlete.id):
        write_athlete(session, User.model_validate(athlete.model_dump()))
    background_tasks.add_task(update_activities, user)
    logger.info("logged in successfully")

    set_auth_cookie(response, user)

    return True





@router.get("/user-settings", response_model=UserSettings)
def get_user(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
) -> UserSettings:
    """Obtains the logged in user's settings from the database.

    :return: The user's settings.
    """
    athlete = get_athlete(session, user.athlete_id)
    logger.info(athlete)
    return UserSettings(
        athlete_id=user.athlete_id,
        start_date=athlete.start_date,
        end_date=athlete.end_date,
    )


@router.post("/user-settings")
def set_user(
    user_settings: UserSettings,
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    """Updates the logged in user's settings in the database.

    :param user_settings: An instance of UserSettings containing the user's ID, start date, and end date.
    """
    athlete = get_athlete(session, user.athlete_id)
    athlete.start_date = user_settings.start_date
    athlete.end_date = user_settings.end_date
    update_athlete(session, athlete)
    logger.info(athlete.end_date)
    delete_activities(session, user.athlete_id)
    activities = get_activity_summaries(
        user, start_date=athlete.start_date, end_date=athlete.end_date
    )
    logger.info(activities[-1])
    write_activities(session, activities)

@router.post("/logout")
def logout(response: Response) -> dict:
    """
    Clear the JWT auth cookie, effectively logging the user out.
    """
    response.set_cookie(
        key="auth_token",
        value="",
        max_age=0,
        expires=0,
        httponly=True,
        samesite="lax",
    )
    return {"detail": "Logged out"}