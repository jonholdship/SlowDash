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
    strava_client_id: int
    strava_client_secret: str
    database_port: int
    port: int  
    redirect_url: str
    frontend_url: str
    # JWT configuration
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    # Long app-session cookie; Strava refresh/revocation controls real re-login.
    jwt_expires_hours: int = 24 * 365 * 30
