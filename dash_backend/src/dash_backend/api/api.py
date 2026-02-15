import json
from fastapi import Depends, FastAPI, HTTPException
import logging
from sqlalchemy.orm import Session
from urllib.parse import unquote

from dash_backend.content.stats import create_training_stats
from dash_backend.content.plots import training_summaries
from dash_backend.models import TokenResponse, UserSettings, HeroStats
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
    athlete, token_response = athlete_login(access_code)
    logger.info(token_response)
    last_retrieved_date = None
    if athlete_exists(session, athlete.id):
        # only grab activities newer than last log in
        last_retrieved_date = get_latest_activity(session, athlete.id)
    else:
        athlete = User.model_validate(athlete.model_dump())
        athlete = write_athlete(session, athlete)
    if not last_retrieved_date:
        last_retrieved_date = athlete.start_date
    activities = get_activity_summaries(token_response, start_date=last_retrieved_date)
    write_activities(session, activities)
    logger.info("logged in successfully")
    return TokenResponse(
        access_token=token_response.get("access_token"),
        refresh_token=token_response.get("refresh_token"),
        expires_at=token_response.get("expires_at"),
    )


def _extract_access_token(token_param: str) -> str:
    """Accept either a raw token string or a JSON serialized AccessInfo object and
    return the access token string to use with stravalib.
    """
    token_str = unquote(token_param)
    parsed = json.loads(token_str)
    logger.info(f"Parsed token_param as JSON: {parsed}")
    return parsed


@app.get("/user-settings", response_model=UserSettings)
def get_user(token: str, session: Session = Depends(get_db)) -> UserSettings:
    """Obtains the logged in user's settings from the database.

    :return: The user's settings.
    """
    try:
        athlete_id = get_athlete_id(_extract_access_token(token))
        logger.info(f"athlete: {athlete_id}")
    except:
        return HTTPException(401, "Token Expired")
    athlete = get_athlete(session, athlete_id)
    logger.info(athlete)
    return UserSettings(
        athlete_id=athlete_id, start_date=athlete.start_date, end_date=athlete.end_date
    )


@app.post("/user-settings")
def set_user(
    user_settings: UserSettings, token: str, session: Session = Depends(get_db)
):
    """Updates the logged in user's settings in the database.

    :param user_settings: An instance of UserSettings containing the user's ID, start date, and end date.
    """
    athlete_id = get_athlete_id(_extract_access_token(token))
    logger.info(user_settings)
    athlete = get_athlete(session, athlete_id)
    athlete.start_date = user_settings.start_date
    athlete.end_date = user_settings.end_date
    update_athlete(session, athlete)
    logger.info(athlete.end_date)
    delete_activities(session, athlete_id)
    access_token = _extract_access_token(token)
    activities = get_activity_summaries(
        access_token, start_date=athlete.start_date, end_date=athlete.end_date
    )
    logger.info(activities[-1])
    write_activities(session, activities)


@app.get("/hero-stats")
def get_hero_stats(token: str, session: Session = Depends(get_db)) -> HeroStats:
    """Get summary statistics for the logged in user. Showing
    how their last four weeks of training compares to the previous four weeks.
    """
    athlete_id = get_athlete_id(_extract_access_token(token))
    activities = get_activities(session, athlete_id=athlete_id)
    hero_stats = create_training_stats(activities=activities)
    return hero_stats


@app.get("/activities-summary")
def activities_summary(token: str, session: Session = Depends(get_db)):
    """
    Returns a table of user activities.
    """
    athlete_id = get_athlete_id(_extract_access_token(token))
    activities = get_activities(session, athlete_id=athlete_id)
    activities = activities.sort_values("start_date", ascending=False)
    activities["Cumulative Distance / km"] = activities["distance"].cumsum()
    activities["Cumulative Duration / min"] = activities["moving_time"].cumsum() / 60.0
    activities["Number of runs"] = range(1, len(activities) + 1)
    df_records = activities.to_dict("records")
    return df_records


@app.get("/activity")
def get_activity(token: str, activity_id: int, session: Session = Depends(get_db)):
    """
    Returns the activity stream for a specific activity given an activity ID.
    """
    access_token = _extract_access_token(token)
    activity_df = get_activity_stream(token_info=access_token, activity_id=activity_id)
    return activity_df.to_dict()


@app.get("/runs")
def get_runs(token: str, session: Session = Depends(get_db)):
    athlete_id = get_athlete_id(_extract_access_token(token))
    activities = get_activities(session, athlete_id=athlete_id)
    activities = activities[
        ["id", "name", "start_date", "distance", "pace", "average_heartrate"]
    ]
    activities["pace"] = activities["pace"].map(pace_to_string)
    return activities.to_dict(orient="records")


@app.get("/summary-plots")
def get_summary_plots(token: str, session: Session = Depends(get_db)):
    athlete_id = get_athlete_id(_extract_access_token(token))
    activities = get_activities(session, athlete_id=athlete_id)
    plots = training_summaries(activities)
    return plots
