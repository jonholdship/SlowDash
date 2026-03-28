from datetime import date, datetime
from pydantic import BaseModel, field_validator


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

    athlete_id: int
    start_date: datetime | None
    end_date: datetime | None
    birthday: date | None = None
    max_hr_override: float | None = None
    hr_zone_highlight: int | None = None


class UserSettingsUpdate(BaseModel):
    start_date: datetime | None = None
    end_date: datetime | None = None
    birthday: date | None = None
    max_hr_override: float | None = None
    hr_zone_highlight: int | None = None

    @field_validator("hr_zone_highlight")
    @classmethod
    def zone_highlight_range(cls, v: int | None) -> int | None:
        if v is None:
            return None
        if v < 1 or v > 5:
            raise ValueError("hr_zone_highlight must be between 1 and 5")
        return v


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
