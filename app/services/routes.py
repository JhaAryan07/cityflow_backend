from typing import Any

from app.services.providers import routing_provider


async def get_vehicle_routes(request: dict[str, Any]) -> list[dict[str, Any]]:
    return await routing_provider.get_route(request)
