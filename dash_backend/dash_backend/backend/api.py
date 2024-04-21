from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException
import logging
from sqlalchemy.orm import Session

from backend.models import TokenResponse, UserSettings
from backend.session import SessionLocal
from backend.strava import (
    athlete_login,
    get_athlete_id,
    get_activity_summaries,
    get_activity_stream,
    get_auth_url,
)
from database.crud import (
    athlete_exists,
    write_athlete,
    delete_activities,
    get_athlete,
    get_latest_activity,
    write_activities,
    get_activities,
    update_athlete,
)

from database import models, schemas

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


@app.get("/login")
def user_login(access_code: str, session: Session = Depends(get_db)) -> TokenResponse:
    """
    Take short lived access code and exchange for token through Strava API.
    Update the database with any activities recorded since last log in.
    """
    athlete, token = athlete_login(access_code)
    if athlete_exists(session, athlete.id):
        # only grab activities newer than last log in
        latest_date = get_latest_activity(session, athlete.id)
        latest_date = latest_date + timedelta(minutes=1)
    else:
        athlete = schemas.User.validate(athlete)
        athlete = write_athlete(session, athlete)
        logger.info(
            f"athlete {athlete.id} exists = {athlete_exists(session,athlete.id)}"
        )
        latest_date = athlete.start_date
    activities = get_activity_summaries(token, start_date=latest_date)
    write_activities(session, activities)
    return TokenResponse(token=token)


@app.get("/user-settings")
def get_user(token: str, session: Session = Depends(get_db)) -> UserSettings:
    try:
        athlete_id = get_athlete_id(token)
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
    logger.info(user_settings)
    athlete = get_athlete(session, user_settings.athlete_id)
    athlete.start_date = user_settings.start_date
    athlete.end_date = user_settings.end_date
    update_athlete(session, athlete)
    logger.info(athlete.end_date)
    delete_activities(session, user_settings.athlete_id)
    activities = get_activity_summaries(
        token, start_date=athlete.start_date, end_date=athlete.end_date
    )
    logger.info(activities[-1])
    write_activities(session, activities)


@app.get("/activities-summary")
def activities_summary(token: str, session: Session = Depends(get_db)):
    """
    Returns a table of user activities.
    """
    try:
        athlete_id = get_athlete_id(token)
    except:
        return HTTPException(401, "Token Expired")
    activities = get_activities(session, athlete_id=athlete_id)
    activities = activities.sort_values("start_date")
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
    try:
        athlete_id = get_athlete(token)
    except:
        return HTTPException(401, "Token Expired")
    activity_df = get_activity_stream(access_token=token, activity_id=activity_id)
    return activity_df.to_dict()
