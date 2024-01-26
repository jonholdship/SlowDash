import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from . import models
from . import schemas


def get_activities(db: Session, athlete_id: int) -> pd.DataFrame:
    query = select(models.Activity).where(models.Activity.user_id == athlete_id)
    return pd.read_sql(query, db.connection())


def get_activity(db: Session, activity_id: int) -> pd.DataFrame:
    query = select(models.Activity).where(models.Activity.id == activity_id)
    return pd.read_sql(query, db.connection())


def get_latest_activity(db: Session, athlete_id: int):
    query = (
        select(models.Activity.start_date)
        .where(models.Activity.user_id == athlete_id)
        .order_by(models.Activity.start_date)
    )
    return db.execute(query).first()[0]


def write_activities(db: Session, activities: list[schemas.Activity]):
    activities = [models.Activity(**activity.dict()) for activity in activities]
    db.add_all(activities)
    db.commit()


def athlete_exists(db: Session, athlete_id: int):
    query = select(models.User.id).where(models.User.id == athlete_id)
    user = db.execute(query).first()
    return user


def write_athlete(db: Session, athlete: schemas.User):
    db_item = models.User(**athlete.__dict__)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def write_activity_stream(db: Session, activity_stream: schemas.ActivityStream):
    return 0
