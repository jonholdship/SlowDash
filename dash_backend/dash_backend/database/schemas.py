from datetime import time, datetime, timedelta
from pydantic import BaseModel, validator, Field
from typing import Any, Optional


def future_date():
    return datetime.today() + timedelta(days=36500)


def past_date():
    return datetime.today() - timedelta(days=90)


class User(BaseModel):
    class Config:
        orm_mode: True

    id: int
    firstname: str
    lastname: str
    start_date: datetime = Field(default_factory=past_date)
    end_date: datetime = Field(default_factory=future_date)
    username: Optional[str]


class Activity(BaseModel):
    id: int
    user_id: int = Field(..., alias="athlete")
    name: str
    distance: float
    moving_time: float
    elapsed_time: float
    total_elevation_gain: float
    type: str
    start_date: datetime
    start_date_local: datetime
    location_city: Optional[str]
    location_country: str
    kudos_count: int
    athlete_count: int
    gear_id: Optional[str]
    average_speed: float
    max_speed: float
    splits_metric: Optional[float]
    splits_standard: Optional[float]
    has_heartrate: bool
    average_heartrate: Optional[float]
    max_heartrate: Optional[float]
    average_cadence: Optional[float]
    device_name: Optional[str]
    calories: Optional[float]
    description: Optional[str]
    workout_type: Optional[str]
    pace: Optional[float]

    @validator("type", pre=True)
    @classmethod
    def workout_type(cls, v) -> str:
        if isinstance(v, str):
            return v
        else:
            return str(v)

    @validator("athlete", "user_id", pre=True, check_fields=False)
    @classmethod
    def unpack_strava_activity(cls, v) -> Any:
        if isinstance(v, int):
            return v
        try:
            return v.__dict__["id"]
        except:
            raise ValueError("Fuck man.")


class ActivityStream(BaseModel):
    id: int
    user_id: int
    time: time
    distance: float
    heartrate: float
    cadence: float
    velocity_smooth: float
    pace: float
