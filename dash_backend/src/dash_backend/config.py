from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_prefix="API_", case_sensitive=False, extra="ignore"
    )

    stats_timedelta: int = 30
    start_date: datetime = datetime.fromisoformat("2023-06-02")
    end_date: datetime = datetime.today()
    max_heartrate: int = 190
    strava_client_id: str
    strava_client_secret: str
    database_port: int
    port: int
    redirect_url: str
