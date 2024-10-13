from datetime import datetime
from pydantic import BaseSettings


class ApiConfig(BaseSettings):
    class Config:
        env_prefix = "API_"
        case_sensitive = False
        env_file = ".env"

    stats_timedelta: int = 30
    start_date: datetime = datetime.fromisoformat("2023-06-02")
    end_date: datetime = datetime.today()
    max_heartrate: int = 190
    strava_client_id: str
    strava_client_secret: str
    database_port: int
    port: int
    redirect_url: str
