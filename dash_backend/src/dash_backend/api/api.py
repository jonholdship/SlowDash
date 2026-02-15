import json
from fastapi import Depends, FastAPI
import logging
import numpy as np
from sqlalchemy.orm import Session
from typing import Annotated


from dash_backend.api.auth import get_current_user
from dash_backend.content.stats import create_training_stats
from dash_backend.content.plots import training_summaries
from dash_backend.models import (
    UserSettings,
    HeroStats,
    AuthenticatedUser,
    TokenResponse,
)
from dash_database.session import SessionLocal
from dash_backend.strava.strava_client import (
    athlete_login,
    get_athlete_id,
    get_activity_summaries,
    get_activity_stream,
    get_auth_url,
)
from dash_backend.strava.strava_utils import pace_to_string
from dash_database.crud import (
    athlete_exists,
    write_athlete,
    delete_activities,
    get_athlete,
    get_latest_activity,
    write_activities,
    get_activities,
    update_athlete,
)

from dash_database.schemas import User

app = FastAPI()

logger = logging.getLogger("uvicorn")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/strava-url")
def strava_auth_url():
    return {"strava_url": get_auth_url()}


@app.get("/login", response_model=TokenResponse)
def user_login(access_code: str, session: Session = Depends(get_db)) -> TokenResponse:
    """
    Take short lived access code and exchange for token through Strava API.
    Update the database with any activities recorded since last log in.
    """
    logger.info("logging in with access code", access_code)
    athlete, user = athlete_login(access_code)
    last_retrieved_date = None
    if athlete_exists(session, athlete.id):
        # only grab activities newer than last log in
        last_retrieved_date = get_latest_activity(session, athlete.id)
    else:
        athlete = User.model_validate(athlete.model_dump())
        athlete = write_athlete(session, athlete)
    if not last_retrieved_date:
        last_retrieved_date = athlete.start_date
    activities = get_activity_summaries(user=user, start_date=last_retrieved_date)
    write_activities(session, activities)
    logger.info("logged in successfully")
    return TokenResponse(
        access_token=user.access_token,
        refresh_token=user.refresh_token,
        expires_at=user.expires_at,
    )


@app.get("/user-settings", response_model=UserSettings)
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


@app.post("/user-settings")
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


@app.get("/hero-stats")
def get_hero_stats(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
) -> HeroStats:
    """Get summary statistics for the logged in user. Showing
    how their last four weeks of training compares to the previous four weeks.
    """
    activities = get_activities(session, athlete_id=user.athlete_id)
    hero_stats = create_training_stats(activities=activities)
    return hero_stats


@app.get("/activities-summary")
def activities_summary(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    """
    Returns a table of user activities.
    """
    activities = get_activities(session, athlete_id=user.athlete_id)
    activities = activities.sort_values("start_date", ascending=False)
    activities["Cumulative Distance / km"] = activities["distance"].cumsum()
    activities["Cumulative Duration / min"] = activities["moving_time"].cumsum() / 60.0
    activities["Number of runs"] = range(1, len(activities) + 1)
    df_records = activities.to_dict("records")
    return df_records


@app.get("/activity")
def get_activity(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    activity_id: int,
    session: Session = Depends(get_db),
):
    """
    Returns the activity stream for a specific activity given an activity ID.
    """
    activity_df = get_activity_stream(user=user, activity_id=activity_id)
    return activity_df.to_dict()


@app.get("/runs")
def get_runs(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    activities = get_activities(session, athlete_id=user.athlete_id)
    activities = activities[
        ["id", "name", "start_date", "distance", "pace", "average_heartrate"]
    ]
    activities["pace"] = activities["pace"].map(pace_to_string)
    activities["start_date"] = activities["start_date"].values.astype(np.int64) // 10**9
    return activities.to_dict(orient="records")


@app.get("/summary-plots")
def get_summary_plots(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    activities = get_activities(session, athlete_id=user.athlete_id)
    plots = training_summaries(activities)
    return plots
