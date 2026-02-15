from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int


class AuthenticatedUser(TokenResponse):
    athlete_id: int


class UserSettings(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda v: v.date().isoformat(),
        }

    start_date: datetime
    end_date: Optional[datetime]

    # @field_serializer("start_date")
    # @field_serializer("end_date")
    # def serialize_date(self, dt: datetime, _info):
    #     return dt.date()


class HeroStats(BaseModel):
    runs: str
    runs_change: str
    runs_trend: str
    pace: str
    pace_change: str
    pace_trend: str
    distance: str
    distance_change: str
    distance_trend: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.date().isoformat(),
        }
