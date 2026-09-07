from typing import Any, Protocol


class TrafficProvider(Protocol):
    async def get_traffic(self, city: str) -> list[dict[str, Any]]: ...


class RoutingProvider(Protocol):
    async def get_route(self, request: dict[str, Any]) -> list[dict[str, Any]]: ...


class TransitProvider(Protocol):
    async def get_network(self, city: str) -> dict[str, Any]: ...
    async def plan_journey(self, request: dict[str, Any]) -> list[dict[str, Any]]: ...


class WeatherProvider(Protocol):
    async def get_weather(self, city: str) -> dict[str, Any]: ...


class IncidentProvider(Protocol):
    async def get_incidents(self, city: str, page: int = 1, page_size: int = 100) -> dict[str, Any]: ...


class SafetyProvider(Protocol):
    async def get_safety(self, city: str, time_of_day: str) -> dict[str, Any]: ...


class PredictionProvider(Protocol):
    """Contract for the future ML prediction provider. No model inference lives here."""
    async def get_traffic_prediction(self, city: str, horizon: int) -> dict[str, Any]: ...
