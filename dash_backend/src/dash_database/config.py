from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class DbConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="POSTGRES_", case_sensitive=False
    )

    db: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    driver: str = "sqlite"
