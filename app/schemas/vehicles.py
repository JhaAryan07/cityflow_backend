from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

VehicleType = Literal["Motorcycle", "Car", "Van", "Bus", "Truck"]


class VehicleBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    vehicle_type: VehicleType
    height_m: float = Field(gt=0, le=10)
    width_m: float = Field(gt=0, le=5)
    length_m: float = Field(gt=0, le=30)
    weight_t: float = Field(gt=0, le=100)


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    vehicle_type: VehicleType | None = None
    height_m: float | None = Field(default=None, gt=0, le=10)
    width_m: float | None = Field(default=None, gt=0, le=5)
    length_m: float | None = Field(default=None, gt=0, le=30)
    weight_t: float | None = Field(default=None, gt=0, le=100)


class Vehicle(VehicleBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
