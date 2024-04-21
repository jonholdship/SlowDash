from datetime import datetime
import numpy as np
import pandas as pd
from stravalib import Client
from stravalib.model import Athlete

from backend.config import ApiConfig

from database import schemas


def get_auth_url() -> str:
    client = Client()
    api_config = ApiConfig()
    return client.authorization_url(
        client_id=api_config.strava_client_id,
        redirect_uri=api_config.redirect_url,
        state="strava-dash-app",
    )


def athlete_login(access_code):
    client = Client()
    api_config = ApiConfig()
    response = client.exchange_code_for_token(
        client_id=api_config.strava_client_id,
        client_secret=api_config.strava_client_secret,
        code=access_code,
    )
    access_token = response["access_token"]
    client = Client(access_token=access_token)

    athlete = client.get_athlete()
    return athlete, access_token


def get_athlete_id(access_token) -> int:
    client = Client(access_token=access_token)
    athlete = client.get_athlete()
    return athlete.id


def get_activity_summaries(
    access_token, start_date, end_date=None, activity_type="Run"
) -> list[schemas.Activity]:
    client = Client(access_token=access_token)

    if end_date is None:
        end_date = datetime.today()
    activities = []
    for activity in client.get_activities(before=end_date, after=start_date):
        if activity.type == activity_type:
            activity = schemas.Activity.validate(activity)
            activity.pace = 1000.0 / (60 * activity.average_speed)
            activities.append(activity)
    return activities


def get_activity_stream(access_token, activity_id):
    client = Client(access_token=access_token)
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
