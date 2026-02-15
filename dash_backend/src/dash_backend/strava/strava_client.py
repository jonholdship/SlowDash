from datetime import datetime
import numpy as np
import pandas as pd
from stravalib import Client
from stravalib.model import DetailedAthlete
from stravalib.protocol import AccessInfo
from dash_backend.config import ApiConfig

from dash_database.schemas import Activity


def get_auth_url() -> str:
    client = Client()
    api_config = ApiConfig()
    return client.authorization_url(
        client_id=api_config.strava_client_id,
        redirect_uri=api_config.redirect_url,
        state="strava-dash-app",
    )


def athlete_login(access_code) -> tuple[DetailedAthlete, AccessInfo]:
    client = Client()
    api_config = ApiConfig()
    token_info: AccessInfo = client.exchange_code_for_token(
        client_id=api_config.strava_client_id,
        client_secret=api_config.strava_client_secret,
        code=access_code,
    )
    # response is the AccessInfo mapping: contains access_token, refresh_token, expires_at
    client = Client(
        access_token=token_info["access_token"],
        token_expires=token_info["expires_at"],
        refresh_token=token_info["refresh_token"],
    )

    athlete = client.get_athlete()
    return athlete, token_info


def _get_client(token_info: AccessInfo) -> Client:
    return Client(
        access_token=token_info["access_token"],
        token_expires=token_info["expires_at"],
        refresh_token=token_info["refresh_token"],
    )


def get_athlete_id(token_info: AccessInfo) -> int:
    client = _get_client(token_info)
    athlete = client.get_athlete()
    return athlete.id


def get_activity_summaries(
    token_info: AccessInfo,
    start_date: datetime,
    end_date: datetime | None = None,
    activity_type: str = "Run",
) -> list[Activity]:
    client = _get_client(token_info)

    if end_date is None:
        end_date = datetime.today()
    activities = []
    for activity in client.get_activities(before=end_date, after=start_date):
        if activity.type == activity_type:
            detailed_activity = client.get_activity(activity.id)
            if detailed_activity is None:
                continue
            activity = Activity.model_validate(detailed_activity.model_dump())
            activities.append(activity)
    return activities


def get_activity_stream(token_info: AccessInfo, activity_id):
    client = _get_client(token_info)
    activity_df = pd.DataFrame()
    for header, stream in client.get_activity_streams(
        str(activity_id),
        types=["time", "distance", "heartrate", "cadence", "velocity_smooth"],
    ).items():
        activity_df[header] = stream.data

    # low speed => incredibly high pace. Let's just clip it to 0 pace.
    activity_df["pace"] = np.where(
        activity_df["velocity_smooth"] > 0.5,
        1000.0 / (activity_df["velocity_smooth"] * 60),
        0,
    )
    return activity_df
