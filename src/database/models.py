from sqlalchemy.orm import declarative_base
from sqlalchemy import String, Float, Integer, TIMESTAMP, Boolean, Column


# declarative base class
SummaryBase = declarative_base()
ActivityBase = declarative_base()


class ActivitySummary(SummaryBase):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    distance = Column(Float)
    moving_time = Column(Float)
    elapsed_time = Column(Float)
    total_elevation_gain = Column(Float)
    start_date = Column(TIMESTAMP)
    start_date_local = Column(TIMESTAMP)
    average_speed = Column(Float)
    max_speed = Column(Float)
    has_heartrate = Column(Boolean)
    average_heartrate = Column(Float)
    max_heartrate = Column(Float)
    average_cadence = Column(Float)
    calories = Column(Float)
    description = Column(String(50))
    workout_type = Column(String(50))
    pace = Column(Float)
    cumulative_distance = Column(Float)
    cumulative_time = Column(Float)
    number_of_runs = Column(Integer)


class ActivityDetail(ActivityBase):
    __tablename__ = "activity_detail"
    id = Column(String, primary_key=True)
    time = Column(Float)
    distance = Column(Float)
    heartrate = Column(Float)
    cadence = Column(Float)
    velocity_smooth = Column(Float)
    pace = Column(Float)
