import logging
import numpy as np
import pandas as pd

from dash_backend.strava.strava_utils import pace_to_string
from dash_backend.models import HeroStats

logger = logging.getLogger("uvicorn")


def create_training_stats(activities: pd.DataFrame):
    summary = (
        activities.groupby(pd.Grouper(key="start_date_local", freq="4W"))
        .agg({"distance": "sum", "pace": "mean", "id": "count"})
        .fillna(0.0)
    ).reset_index()

    stats_dict = {
        "runs": f"{summary.iloc[-1]["id"]}",
        "runs_change": f"{np.abs(summary.iloc[-1]["id"] - summary.iloc[-2]["id"])}",
        "runs_trend": (
            "up" if summary.iloc[-1]["id"] > summary.iloc[-2]["id"] else "down"
        ),
        "pace": pace_to_string(summary.iloc[-1]["pace"]),
        "pace_change": pace_to_string(
            np.abs(summary.iloc[-1]["pace"] - summary.iloc[-2]["pace"])
        ),
        "pace_trend": (
            "up" if summary.iloc[-1]["pace"] < summary.iloc[-2]["pace"] else "down"
        ),
        "distance": f"{summary.iloc[-1]["distance"]:.1} km",
        "distance_change": f"{np.abs(summary.iloc[-1]["distance"] - summary.iloc[-2]["distance"]):.1f} km",
        "distance_trend": (
            "up"
            if summary.iloc[-1]["distance"] > summary.iloc[-2]["distance"]
            else "down"
        ),
    }
    return HeroStats.model_validate(stats_dict)
