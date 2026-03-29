"""Heart rate zones as fixed percentages of effective max HR."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel

HrZoneSource = Literal["override", "formula", "config_default"]

# Five zones: from runners world
#https://www.runnersworld.com/uk/training/beginners/a760176/heart-rate-training-the-basics/
_ZONE_FRACTIONS: list[tuple[int, str, float, float]] = [
    (1, "Z1", 0.20, 0.60),
    (2, "Z2", 0.60, 0.70),
    (3, "Z3", 0.70, 0.80),
    (4, "Z4", 0.80, 0.93),
    (5, "Z5", 0.94, 1.00),
]


class HrZoneBand(BaseModel):
    id: int
    label: str
    min_bpm: int
    max_bpm: int


class HrZonesPayload(BaseModel):
    effective_max_hr: int
    source: HrZoneSource
    zones: list[HrZoneBand]


def _age_years(birthday: date, today: date | None = None) -> int:
    if today is None:
        today = date.today()
    years = today.year - birthday.year
    if (today.month, today.day) < (birthday.month, birthday.day):
        years -= 1
    return max(0, years)


def effective_max_hr(
    *,
    birthday: date | None,
    max_hr_override: float | None,
    config_default: int,
) -> tuple[int, HrZoneSource]:
    if max_hr_override is not None:
        clamped = max(120, min(220, round(max_hr_override)))
        return clamped, "override"
    if birthday is not None:
        age = _age_years(birthday)
        return round(211 - 0.64 * age), "formula"
    return config_default, "config_default"


def zones_for_max_hr(max_hr: int) -> list[HrZoneBand]:
    bands: list[HrZoneBand] = []
    for zid, label, lo, hi in _ZONE_FRACTIONS:
        min_bpm = max(1, round(max_hr * lo))
        max_bpm = max(min_bpm, round(max_hr * hi))
        bands.append(HrZoneBand(id=zid, label=label, min_bpm=min_bpm, max_bpm=max_bpm))
    return bands


def build_hr_zones_payload(
    *,
    birthday: date | None,
    max_hr_override: float | None,
    config_default: int,
) -> HrZonesPayload:
    mx, src = effective_max_hr(
        birthday=birthday,
        max_hr_override=max_hr_override,
        config_default=config_default,
    )
    return HrZonesPayload(
        effective_max_hr=mx,
        source=src,
        zones=zones_for_max_hr(mx),
    )
