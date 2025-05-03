from sqlalchemy import create_engine, Engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from dash_database import models
from dash_database.config import DbConfig


def new_engine() -> Engine:
    db_config = DbConfig()
    url = URL.create(
        drivername=db_config.driver,
        username=db_config.user,
        host=db_config.host,
        database=db_config.db,
        port=db_config.port,
        password=db_config.password,
    )
    print("url", url)
    return create_engine(url)


engine = new_engine()
engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
print("Database tables created successfully.")
