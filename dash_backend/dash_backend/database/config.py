from pydantic import BaseSettings


class DbConfig(BaseSettings):
    class Config:
        env_prefix = "POSTGRES_"
        case_sensitive = False
        env_file = ".env"

    db: str
    user: str
    password: str
    host: str
    port: str
    driver: str
