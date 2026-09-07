from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal


class VehiclePayload(BaseModel):
    vehicle_type: Literal["Motorcycle", "Car", "Van", "Bus", "Truck"]
    height_m: float = Field(gt=0, le=10)
    width_m: float = Field(gt=0, le=5)
    length_m: float = Field(gt=0, le=30)
    weight_t: float = Field(gt=0, le=100)


class VehicleRouteRequest(BaseModel):
    origin: str = Field(min_length=1, max_length=255)
    destination: str = Field(min_length=1, max_length=255)
    vehicle: VehiclePayload
    preference: Literal["balanced", "fit", "emission"] = "balanced"


class RouteOption(BaseModel):
    id: str
    label: str
    geometry: list[tuple[float, float]]
    duration_min: int
    distance_km: float
    estimated_co2_kg: float
    suitability_score: int = Field(ge=0, le=100)
    restrictions: list[str] = []
    recommendation_reason: str


class SavedRouteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    origin: str = Field(min_length=1, max_length=255)
    destination: str = Field(min_length=1, max_length=255)
    vehicle_profile_id: UUID | None = None
    preference: Literal["balanced", "fit", "emission"] = "balanced"


class SavedRoute(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    origin: str
    destination: str
    vehicle_profile_id: UUID | None = None
    preference: str
