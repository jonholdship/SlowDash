from datetime import time, datetime, timedelta
from pydantic import BaseModel, Field, field_validator
from typing import Any


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
    username: str | None


class Activity(BaseModel):
    id: int
    user_id: int = Field(..., alias="athlete")
    name: str | None
    distance: float | None
    moving_time: float | None
    elapsed_time: float | None
    total_elevation_gain: float | None
    type: str | None
    start_date: datetime | None
    start_date_local: datetime | None
    location_city: str | None
    location_country: str | None
    kudos_count: int | None
    athlete_count: int | None
    gear_id: str | None
    average_speed: float | None
    max_speed: float | None
    # splits_metric: float | None
    # splits_standard: float | None
    has_heartrate: bool | None
    average_heartrate: float | None
    max_heartrate: float | None
    average_cadence: float | None
    device_name: str | None
    calories: float | None
    description: str | None
    workout_type: str | None = Field(default="Run")
    pace: float | None = Field(default=0.0)

    @field_validator("type", "workout_type", mode="before")
    @classmethod
    def workout_type(cls, v) -> str:
        if isinstance(v, str):
            return v
        else:
            return str(v)

    @field_validator("athlete", "user_id", mode="before", check_fields=False)
    @classmethod
    def unpack_strava_activity(cls, v) -> Any:
        if isinstance(v, int):
            return v
        if isinstance(v, dict):
            return v["id"]
        try:
            return v.id
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
