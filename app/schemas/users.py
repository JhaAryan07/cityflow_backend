from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserPreferenceUpdate(BaseModel):
    default_vehicle_id: UUID | None = None
    preferred_route_type: str = Field(default="balanced", pattern="^(balanced|fit|emission)$")
    units: str = Field(default="metric", pattern="^(metric|imperial)$")


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    auth_provider_user_id: str
    name: str
    email: str
    avatar_url: str | None = None
    role: str
