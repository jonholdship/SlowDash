from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.config import ApiConfig
from backend.models import TokenResponse
from backend.session import SessionLocal
from backend.strava import (
    athlete_login,
    get_athlete,
    get_activity_summaries,
    get_activity_stream,
    get_auth_url,
)
from database.crud import (
    athlete_exists,
    write_athlete,
    get_latest_activity,
    write_activities,
    get_activities,
)

from database import schemas

app = FastAPI()


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
    athlete, token = athlete_login(access_code)
    if athlete_exists(session, athlete.id):
        # only grab activities newer than last log in
        latest_date = get_latest_activity(session, athlete.id)
        latest_date = latest_date + timedelta(minutes=1)
    else:
        athlete = schemas.User.validate(athlete)
        write_athlete(session, athlete)
        api_config = ApiConfig()
        latest_date = api_config.start_date
    activities = get_activity_summaries(token, start_date=latest_date)
    write_activities(session, activities)
    return TokenResponse(token=token)


@app.get("/activities-summary")
def activities_summary(token: str, session: Session = Depends(get_db)):
    athlete_id = get_athlete(token)
    print(athlete_id)
    activities = get_activities(session, athlete_id=athlete_id)
    print(activities)
    activities = activities.sort_values("start_date")
    activities["Cumulative Distance / km"] = activities["distance"].cumsum()
    activities["Cumulative Duration / min"] = activities["moving_time"].cumsum()
    activities["Number of runs"] = range(1, len(activities) + 1)
    df_records = activities.to_dict("records")
    print(df_records)
    return df_records


@app.get("/activity")
def get_activity(token: str, activity_id: int, session: Session = Depends(get_db)):
    activity_df = get_activity_stream(access_token=token, activity_id=activity_id)
    return activity_df.to_dict()
