from pydantic import BaseSettings
from typing import Optional


class DbConfig(BaseSettings):
    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = False
        env_file = ".env"

    db: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    driver: str = "sqlite"
