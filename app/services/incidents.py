from typing import Any

from app.services.providers import incident_provider


async def list_incidents(city: str, page: int = 1, page_size: int = 100) -> dict[str, Any]:
    return await incident_provider.get_incidents(city, page, page_size)
