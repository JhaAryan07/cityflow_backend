import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import Depends, Header, HTTPException

from app.core.config import settings

DEMO_USER = {
    "id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
    "name": "CityFlow Demo",
    "email": "demo@cityflow.local",
    "avatar_url": None,
    "role": "CITIZEN",
}


async def get_current_user(authorization: str | None = Header(default=None)) -> dict[str, Any]:
    if not settings.auth_enabled:
        return DEMO_USER
    if settings.auth_mode == "mock" and authorization == "Bearer mock-token":
        return DEMO_USER
    raise HTTPException(status_code=401, detail={"error": {"code": "UNAUTHENTICATED", "message": "Authentication required"}})


def require_role(*allowed_roles: str) -> Callable[..., Awaitable[dict[str, Any]]]:
    async def dependency(user: dict[str, Any] = Depends(get_current_user)) -> dict[str, Any]:
        if user.get("role") not in allowed_roles:
            raise HTTPException(status_code=403, detail={"error": {"code": "FORBIDDEN", "message": "You do not have permission for this operation"}})
        return user

    return dependency
