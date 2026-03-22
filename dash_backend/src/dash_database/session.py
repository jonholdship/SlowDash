from sqlalchemy import create_engine, Engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dash_database import models
from dash_database.config import DbConfig


def get_engine_url() -> URL:
    db_config = DbConfig()
    return URL.create(
        drivername=db_config.driver,
        username=db_config.user,
        host=db_config.host,
        database=db_config.db,
        port=db_config.port,
        password=db_config.password,
    )


def new_engine() -> Engine:
    return create_engine(get_engine_url())


engine = new_engine()
engine.connect()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
