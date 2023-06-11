from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)
import numpy as np
import pandas as pd
import datetime
import os
from pathlib import Path


SUMMARY_COLUMNS = [
    "activityId",
    "startTimeGMT",
    "distance",
    "duration",
    "elapsedDuration",
    "movingDuration",
    "elevationGain",
    "elevationLoss",
    "averageSpeed",
    "maxSpeed",
    "calories",
    "bmrCalories",
    "averageHR",
    "maxHR",
    "averageRunningCadenceInStepsPerMinute",
    "maxRunningCadenceInStepsPerMinute",
    "vO2MaxValue",
]


DATA_ROOT = Path("data/")
ACTIVITY_PATH = DATA_ROOT / "activities/"
os.makedirs(ACTIVITY_PATH, exist_ok=True)
# garmin = Garmin(GARMIN_EMAIL, GARMIN_PASS)
# garmin.login()


# #
# df = pd.read_csv("test.csv")
# df["pace"] = 1000.0 / (60 * df["averageSpeed"])
# df["Cumulative Distance / km"] = df["distance"].cumsum() / 1000.0
# df["dist_grouping"] = (df["Cumulative Distance / km"] / 25).astype(int) * 25


class GarminHelper:
    def __init__(self, username, password, start_date, end_date, max_heartrate):
        self.client = self.garmin_login(username, password)
        self.activities = os.listdir(ACTIVITY_PATH)
        self.activity_summary = self.get_activities_summary(start_date, end_date)

    def garmin_login(self, username, password):
        try:
            garmin = Garmin(username, password)
            garmin.login()
            return garmin
        except (
            GarminConnectConnectionError,
            GarminConnectAuthenticationError,
            GarminConnectTooManyRequestsError,
        ) as err:
            print("login fail")
            print("Error occurred during Garmin Connect Client init: %s" % err)
            quit()
        except Exception:  # pylint: disable=broad-except
            print("Unknown error occurred during Garmin Connect Client init")
            quit()

    def get_activities_summary(self, start_date, end_date, activity_type="running"):
        if end_date == "today":
            end_date = str(datetime.date.today())
        file_path = DATA_ROOT / f"{start_date}-{end_date}.csv"
        if os.path.exists(file_path):
            df = pd.read_parquet(file_path)
            print("read")
        else:
            df = pd.DataFrame(
                self.client.get_activities_by_date(
                    start_date, end_date, activitytype=activity_type
                )
            )[SUMMARY_COLUMNS]
            df.to_parquet(file_path, index=False)

        df = self.augment_activities_summary(df)
        return df

    def augment_activities_summary(self, df):
        df["pace"] = 1000.0 / (60 * df["averageSpeed"])
        df["Cumulative Distance / km"] = df["distance"].cumsum() / 1000.0
        df["dist_grouping"] = (df["Cumulative Distance / km"] / 25).astype(int) * 25
        return df

    def get_activity_data(self, activity_id):
        activity_path = ACTIVITY_PATH / f"{activity_id:.0f}"
        if activity_id in self.activities:
            activity_df = pd.read_parquet(activity_path)
        else:
            activity_json = self.client.get_activity_details(activity_id)
            columns = [x["key"] for x in activity_json["metricDescriptors"]]
            data = pd.DataFrame(activity_json["activityDetailMetrics"])[
                "metrics"
            ].to_list()
            activity_df = pd.DataFrame(columns=columns, data=data)

            # duration in minutes
            activity_df["duration"] = activity_df["sumDuration"] / 60.0

            # stop pace ballooning by just setting to 0 when speed is
            activity_df["pace"] = np.where(
                activity_df["directSpeed"] > 0.1,
                1000.0 / (60 * activity_df["directSpeed"]),
                0,
            )

            # same for elevationPace
            activity_df["elevationPace"] = 1000.0 / (
                60.0
                * np.sqrt(
                    activity_df["directVerticalSpeed"].pow(2)
                    + activity_df["directSpeed"].pow(2)
                )
            )
            activity_df["elevationPace"] = np.where(
                activity_df["directSpeed"] > 0 / 1, activity_df["elevationPace"], 0
            )

            activity_df.to_parquet(activity_path, index=False)
            self.activities.append(activity_id)
        return activity_df
