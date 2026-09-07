from pydantic import BaseModel, Field
from uuid import UUID


class Coordinates(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class UserIdentity(BaseModel):
    id: UUID
    name: str
    email: str
    avatar_url: str | None = None
    role: str = "CITIZEN"


def validate_city(value: str) -> str:
    normalized = value.lower().strip().replace("_", "-")
    # Kept for backwards compatibility with the current frontend query params.
    # Delhi NCR is now the only supported region.
    if normalized not in {"delhi", "delhi-ncr", "delhi ncr"}:
        raise ValueError("CityFlow currently supports Delhi NCR only")
    return "delhi"
