from pydantic import BaseModel, Field
from typing import Literal

TransitMode = Literal["best", "metro", "bus", "rail", "mixed"]


class JourneyRequest(BaseModel):
    origin: str = Field(min_length=1, max_length=255)
    destination: str = Field(min_length=1, max_length=255)
    mode: TransitMode


class Leg(BaseModel):
    mode: Literal["Metro", "Bus", "Rail", "Walk"]
    line: str
    origin: str
    destination: str
    duration: int = Field(ge=0)
    stops: int = Field(ge=0)


class Journey(BaseModel):
    id: str
    mode: TransitMode
    duration: int
    transfers: int = Field(ge=0)
    fare: float = Field(ge=0)
    label: str
    legs: list[Leg]
    origin: str
    destination: str
    geometry: list[tuple[float, float]] = []


class TransitLine(BaseModel):
    name: str
    color: str
    stations: int
    status: str
    mode: Literal["metro", "bus", "rail"]
    connections: list[str]


class Airport(BaseModel):
    name: str
    code: str
    kind: str
    connections: list[str]


class TransitNetwork(BaseModel):
    city: str
    metro: list[TransitLine]
    bus: dict[str, int]
    rail: dict[str, int]
    airports: list[Airport]
