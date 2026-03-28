import json
from fastapi import Depends, Response
from fastapi.background import BackgroundTasks
from fastapi import APIRouter 
import logging
import numpy as np
from sqlalchemy.orm import Session
from typing import Annotated


from dash_backend.api.auth import get_current_user, set_auth_cookie
from dash_backend.content.stats import create_training_stats
from dash_backend.content.plots import training_summaries
from dash_backend.models import HeroStats, AuthenticatedUser, TokenResponse
from dash_database.session import SessionLocal
from dash_backend.strava.strava_client import (
    athlete_login,
    get_activity_summaries,
    get_activity_details,
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

logger = logging.getLogger("uvicorn")
router = APIRouter(prefix="/activities", tags=["activities"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.get("/hero-stats")
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


@router.get("/activities-summary")
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


@router.get("/activity")
def get_activity(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    activity_id: int,
):
    """
    Returns activity details (name, polyline, description, start_date, calories)
    and activity streams (time, distance, heartrate, pace, altitude, etc.) for a given activity ID.
    """
    details = get_activity_details(user=user, activity_id=activity_id)
    activity_df = get_activity_stream(user=user, activity_id=activity_id)
    return {
        "activity": details,
        "streams": activity_df.to_dict("list"),
    }


@router.get("/runs")
def get_runs(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    activities = get_activities(session, athlete_id=user.athlete_id)
    activities = activities.sort_values("start_date", ascending=False)
    activities = activities[
        ["id", "name", "start_date", "distance", "pace", "average_heartrate"]
    ]
    activities["pace"] = activities["pace"].map(pace_to_string)
    activities["start_date"] = activities["start_date"].values.astype(np.int64) // 10**9
    return activities.to_dict(orient="records")


@router.get("/summary-plots")
def get_summary_plots(
    user: Annotated[AuthenticatedUser, Depends(get_current_user)],
    session: Session = Depends(get_db),
):
    activities = get_activities(session, athlete_id=user.athlete_id)
    plots = training_summaries(activities)
    return plots
