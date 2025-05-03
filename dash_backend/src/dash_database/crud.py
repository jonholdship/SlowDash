from datetime import datetime
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import NoSuchTableError, OperationalError
from sqlalchemy import select, delete
from typing import Optional
from . import models
from . import schemas


def get_activities(db: Session, athlete_id: int) -> pd.DataFrame:
    query = select(models.Activity).where(models.Activity.user_id == athlete_id)
    return pd.read_sql(query, db.connection())


def get_activity(db: Session, activity_id: int) -> pd.DataFrame:
    query = select(models.Activity).where(models.Activity.id == activity_id)
    return pd.read_sql(query, db.connection())


def get_latest_activity(db: Session, athlete_id: int) -> Optional[datetime]:
    query = (
        select(models.Activity.start_date)
        .where(models.Activity.user_id == athlete_id)
        .order_by(models.Activity.start_date)
    )
    latest_date = db.execute(query).first()
    if latest_date:
        return latest_date[0]


def write_activities(db: Session, activities: list[schemas.Activity]):
    activities = [models.Activity(**activity.model_dump()) for activity in activities]
    db.add_all(activities)
    db.commit()
    db.flush()


def athlete_exists(db: Session, athlete_id: int):
    query = select(models.User.id).where(models.User.id == athlete_id)
    try:
        db.execute(query).one()
        return True
    except (NoResultFound, OperationalError, NoSuchTableError) as e:
        print(e)
        return False


def delete_activities(db: Session, athlete_id: int):
    query = delete(models.Activity).where(models.Activity.user_id == athlete_id)
    db.execute(query)
    db.commit()
    db.flush()


def get_athlete(db: Session, athlete_id: int) -> models.User:
    df_query = select(models.User)
    df = pd.read_sql(df_query, con=db.connection())
    print(df)
    query = select(models.User).where(models.User.id == athlete_id)
    # for unknown reasons, sqlalchemy returns a tuple of (object,None)
    user = db.execute(query).one()[0]
    return user


def update_athlete(db: Session, athlete: models.User):
    db.add(athlete)
    db.commit()
    db.flush()


def write_athlete(db: Session, athlete: schemas.User):
    db_item = models.User(**athlete.__dict__)
    db.add(db_item)
    db.commit()
    db.flush()
    db.refresh(db_item)
    return db_item


def write_activity_stream(db: Session, activity_stream: schemas.ActivityStream):
    return 0
