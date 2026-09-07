from typing import Any

from app.services.providers import incident_provider, safety_provider, traffic_provider, weather_provider


async def get_network(city: str) -> dict[str, Any]:
    import asyncio

    traffic, incidents, safety, weather = await asyncio.gather(
        traffic_provider.get_traffic(city),
        incident_provider.get_incidents(city, 1, 100),
        safety_provider.get_safety(city, "evening"),
        weather_provider.get_weather(city),
    )
    return {"city": city, "traffic": traffic, "incidents": incidents["items"], "safety": safety["hotspots"], "weather": weather}
