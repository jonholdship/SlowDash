from datetime import time, datetime, timedelta
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Any, Self
from stravalib import unit_helper
from stravalib.model import RelaxedActivityType


def future_date():
    return datetime.today() + timedelta(days=36500)


def past_date():
    return datetime.today() - timedelta(days=365)


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
    average_speed: float | None  # m/s
    max_speed: float | None  # m/s
    has_heartrate: bool | None
    average_heartrate: float | None
    max_heartrate: float | None
    average_cadence: float | None
    device_name: str | None
    calories: float | None
    description: str | None
    pace: float | None = Field(default=None)  # min/km

    @field_validator("distance", mode="before")
    def distance_to_km(distance) -> float:
        return unit_helper.kilometers(distance).magnitude

    @field_validator("type", mode="before")
    def workout_type(v) -> str:
        if isinstance(v, str):
            return v
        elif isinstance(v, RelaxedActivityType):
            return v.root
        else:
            return str(v)

    @field_validator("athlete", "user_id", mode="before", check_fields=False)
    def unpack_strava_activity(v) -> Any:
        if isinstance(v, int):
            return v
        if isinstance(v, dict):
            return v["id"]
        try:
            return v.id
        except:
            raise ValueError("Fuck man.")

    @model_validator(mode="after")
    def check_pace(self) -> Self:
        if (not self.pace) and (self.average_speed):
            self.pace = 1.0 / (self.average_speed * 60 / 1000.0)
        return self


class ActivityStream(BaseModel):
    id: int
    user_id: int
    time: time
    distance: float
    heartrate: float
    cadence: float
    velocity_smooth: float
    pace: float
