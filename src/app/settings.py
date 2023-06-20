import yaml
import datetime
from dotenv import dotenv_values


with open("config.yaml") as f:
    config = {**yaml.load(f, Loader=yaml.FullLoader), **dotenv_values()}


MAX_HR = config["max_heartrate"]

START_DATE = f"{config['start_date']}T00:00:00Z"

if config["end_date"] == "today":
    END_DATE = datetime.datetime.today()
else:
    END_DATE = f"{config['end_date']}T00:00:00Z"
STRAVA_CLIENT_ID = config["STRAVA_CLIENT_ID"]
STRAVA_CLIENT_SECRET = config["STRAVA_CLIENT_SECRET"]
APP_URL = config["APP_URL"]
