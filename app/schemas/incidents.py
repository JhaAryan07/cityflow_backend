from pydantic import BaseModel, Field
from typing import Literal


class IncidentCreate(BaseModel):
    type: str = Field(min_length=1, max_length=60)
    road: str = Field(min_length=1, max_length=255)
    severity: Literal["High", "Medium", "Low"]
    impact: str = Field(min_length=1, max_length=120)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class IncidentStatusUpdate(BaseModel):
    status: Literal["REPORTED", "VERIFIED", "ACTIVE", "MITIGATED", "CLOSED"]


class IncidentResponse(IncidentCreate):
    id: str
    status: str
