from datetime import datetime, timedelta
import logging
import pandas as pd

from dash_backend.config import ApiConfig
from dash_backend.strava.strava_utils import pace_to_string

logger = logging.getLogger("uvicorn")


def pace_stats(
    this_period: pd.DataFrame, last_period: pd.DataFrame
) -> tuple[str, str, str]:
    new_pace = this_period["pace"].dropna().mean()
    old_pace = last_period["pace"].dropna().mean()
    if pd.isna(new_pace):
        new_pace = 0.0
    if pd.isna(old_pace):
        old_pace = 0.0
    logger.info(new_pace, old_pace)
    pace_str = pace_to_string(new_pace)
    pace_change = pace_to_string(new_pace - old_pace)
    pace_trend = "up" if new_pace >= old_pace else "down"
    return pace_str, pace_change, pace_trend


def create_training_stats(activities: pd.DataFrame):
    period_start = datetime.today() - timedelta(days=ApiConfig().stats_timedelta)
    comparison = period_start - timedelta(days=ApiConfig().stats_timedelta)
    this_period = activities[activities["start_date"] > period_start]
    last_period = activities[
        (activities["start_date"] <= period_start)
        & (activities["start_date"] > comparison)
    ]
    pace, pace_change, pace_trend = pace_stats(
        this_period=this_period, last_period=last_period
    )

    return {
        "runs": f"{len(this_period)}",
        "runs_change": f"{len(this_period)-len(last_period)}",
        "runs_trend": "up" if len(this_period) >= len(last_period) else "down",
        "pace": pace,
        "pace_change": pace_change,
        "pace_trend": pace_trend,
        "distance": f"{this_period['distance'].sum()/1000:.1f} km",
        "distance_change": f"{(this_period['distance'].sum()-last_period['distance'].sum())/1000:.1f} km",
        "distance_trend": (
            "up"
            if this_period["distance"].sum() >= last_period["distance"].sum()
            else "down"
        ),
    }
