from stravalib import Client
from stravalib.exc import AccessUnauthorized
import numpy as np
import pandas as pd
import os
from pathlib import Path


SUMMARY_COLUMNS = [
    "id",
    "name",
    "distance",
    "moving_time",
    "elapsed_time",
    "total_elevation_gain",
    "type",
    "start_date",
    "start_date_local",
    "location_city",
    "location_country",
    "kudos_count",
    "athlete_count",
    "gear_id",
    "average_speed",
    "max_speed",
    "splits_metric",
    "splits_standard",
    "has_heartrate",
    "average_heartrate",
    "max_heartrate",
    "average_cadence",
    "device_name",
    "calories",
    "description",
    "workout_type",
]


DATA_ROOT = Path("data/")
ACTIVITY_PATH = DATA_ROOT / "activities/"
os.makedirs(ACTIVITY_PATH, exist_ok=True)


class User:
    def __init__(self, strava_auth):
        client = Client(access_token=strava_auth["access_token"])
        try:
            athlete = client.get_athlete()
            self.firstname = athlete.firstname
            self.lastname = athlete.lastname
            self.id = athlete.id
            self.access_token = strava_auth["access_token"]
            self.authorized = True
        except AccessUnauthorized:
            strava_auth = None
            self.authorized = False
        self.activities = os.listdir(ACTIVITY_PATH)

    def get_activities_summary(self, start_date, end_date, activity_type="Run"):
        file_path = DATA_ROOT / f"{start_date[:10]}.pq"
        if os.path.exists(file_path):
            df = pd.read_parquet(file_path)
        else:
            client = Client(access_token=self.access_token)
            df = self.get_strava_activity_data(
                client, start_date, end_date, activity_type
            )
            df = self.augment_activities_summary(df)
            df.to_parquet(file_path, index=False)
        return df

    def get_strava_activity_data(self, client, start_date, end_date, activity_type):
        meta_data = []
        print(start_date, end_date, "here")
        for activity in client.get_activities(before=end_date, after=start_date):
            if activity.type == activity_type:
                # get meta_data
                meta_data.append(
                    [
                        activity.id,
                        activity.name,
                        activity.distance.magnitude,
                        activity.moving_time,
                        activity.elapsed_time,
                        activity.total_elevation_gain.magnitude,
                        activity.type,
                        activity.start_date,
                        activity.start_date_local,
                        activity.location_city,
                        activity.location_country,
                        activity.kudos_count,
                        activity.athlete_count,
                        activity.gear_id,
                        activity.average_speed.magnitude,
                        activity.max_speed.magnitude,
                        activity.splits_metric,
                        activity.splits_standard,
                        activity.has_heartrate,
                        activity.average_heartrate,
                        activity.max_heartrate,
                        activity.average_cadence,
                        activity.device_name,
                        activity.calories,
                        activity.description,
                        activity.workout_type,
                    ]
                )
        return pd.DataFrame(columns=SUMMARY_COLUMNS, data=meta_data)

    def augment_activities_summary(self, df):
        df["pace"] = 1000.0 / (60 * df["average_speed"])
        df["Cumulative Distance / km"] = df["distance"].cumsum() / 1000.0
        df["Cumulative Duration / min"] = (
            pd.to_timedelta(df["elapsed_time"]).dt.total_seconds().cumsum()
        ) / 60.0
        df["Number of runs"] = df.index + 1
        return df

    def get_activity_data(self, activity_id):
        activity_path = ACTIVITY_PATH / f"{activity_id:.0f}"
        if activity_id in self.activities:
            activity_df = pd.read_parquet(activity_path)
        else:
            client = Client(access_token=self.access_token)
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

            activity_df.to_parquet(activity_path, index=False)
            self.activities.append(activity_id)
        return activity_df
