from datetime import datetime
from pydantic import BaseSettings


class AppConfig(BaseSettings):
    class Config:
        env_prefix = "APP_"
        case_sensitive = False
        env_file = ".env"

    start_date: datetime = datetime.fromisoformat("2023-06-02")
    end_date: datetime = datetime.today()
    max_heartrate: int = 190
    api_url: str
    app_title: str
