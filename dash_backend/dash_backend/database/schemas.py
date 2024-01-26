from datetime import time, datetime
from pydantic import BaseModel, validator, Field
from typing import Any, Optional


class User(BaseModel):
    class Config:
        orm_mode: True

    id: int
    firstname: str
    lastname: str
    username: str


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
    gear_id: str
    average_speed: float
    max_speed: float
    splits_metric: Optional[float]
    splits_standard: Optional[float]
    has_heartrate: bool
    average_heartrate: float
    max_heartrate: float
    average_cadence: float
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
