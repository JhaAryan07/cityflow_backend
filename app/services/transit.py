from typing import Any

from app.services.providers import transit_provider


async def get_network(city: str) -> dict[str, Any]:
    return await transit_provider.get_network(city)


async def plan_journey(request: dict[str, Any]) -> list[dict[str, Any]]:
    return await transit_provider.plan_journey(request)
