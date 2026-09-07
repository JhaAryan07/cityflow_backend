from pydantic import BaseModel, Field
from typing import Literal


class TrafficSegment(BaseModel):
    id: str
    name: str
    coords: list[tuple[float, float]]
    current_speed: float = Field(ge=0)
    free_flow: float = Field(gt=0)
    level: Literal["light", "moderate", "heavy"]


class Incident(BaseModel):
    id: str
    type: str
    road: str
    severity: Literal["High", "Medium", "Low"]
    minutes: int = Field(ge=0)
    impact: str
    coords: tuple[float, float]
    status: str = "ACTIVE"


class Risk(BaseModel):
    id: str
    name: str
    score: int = Field(ge=0, le=100)
    peak: str
    count: int = Field(ge=0)
    coords: tuple[float, float]
    factors: list[str]


class Weather(BaseModel):
    temp: float
    aqi: int = Field(ge=0)
    rain: float = Field(ge=0)
    wind: float = Field(ge=0)
    condition: str
    adjustment: float = Field(ge=0)


class NetworkResponse(BaseModel):
    city: str
    traffic: list[TrafficSegment]
    incidents: list[Incident]
    safety: list[Risk]
    weather: Weather
