from sqlalchemy.ext.declarative import declarative_base


from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    BigInteger,
    String,
    Float,
    DateTime,
    Time,
)
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    activities = relationship("Activity", back_populates="user")


class Activity(Base):
    __tablename__ = "activities"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    user = relationship("User", back_populates="activities")
    name = Column(String)
    distance = Column(Float)
    moving_time = Column(Float)
    elapsed_time = Column(Float)
    total_elevation_gain = Column(Float)
    type = Column(String)
    start_date = Column(DateTime)
    start_date_local = Column(DateTime)
    location_city = Column(String)
    location_country = Column(String)
    kudos_count = Column(Integer)
    athlete_count = Column(Integer)
    gear_id = Column(String)
    average_speed = Column(Float)
    max_speed = Column(Float)
    splits_metric = Column(Float)
    splits_standard = Column(Float)
    has_heartrate = Column(Boolean)
    average_heartrate = Column(Float)
    max_heartrate = Column(Float)
    average_cadence = Column(Float)
    device_name = Column(String)
    calories = Column(Float)
    description = Column(String)
    workout_type = Column(String)
    pace = Column(Float)


class ActivityStream(Base):
    __tablename__ = "activitystreams"
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"))
    time = Column(Time)
    distance = Column(Float)
    heartrate = Column(Float)
    cadence = Column(Float)
    velocity_smooth = Column(Float)
    pace = Column(Float)
