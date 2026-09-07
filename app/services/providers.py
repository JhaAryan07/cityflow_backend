from app.core.config import settings
from app.providers.live import OpenMeteoProvider, TomTomIncidentProvider, TomTomRoutingProvider, TomTomTrafficProvider
from app.providers.mock import (
    MockIncidentProvider,
    MockPredictionProvider,
    MockRoutingProvider,
    MockSafetyProvider,
    MockTrafficProvider,
    MockTransitProvider,
    MockWeatherProvider,
)


def _build_provider(real_cls, mock_cls):
    if settings.provider_mode == "mock":
        return mock_cls()
    return real_cls()


# The hybrid mode makes local development practical before every provider is configured:
# traffic/incidents/weather/routing use live APIs when enabled; transit/safety/prediction remain
# deterministic until their datasets/models are installed.
if settings.provider_mode == "mock":
    traffic_provider = MockTrafficProvider()
    incident_provider = MockIncidentProvider()
    weather_provider = MockWeatherProvider()
    routing_provider = MockRoutingProvider()
else:
    traffic_provider = _build_provider(TomTomTrafficProvider, MockTrafficProvider)
    incident_provider = _build_provider(TomTomIncidentProvider, MockIncidentProvider)
    weather_provider = _build_provider(OpenMeteoProvider, MockWeatherProvider)
    routing_provider = _build_provider(TomTomRoutingProvider, MockRoutingProvider)

if settings.provider_mode in {"live", "hybrid"}:
    transit_provider = MockTransitProvider()
    safety_provider = MockSafetyProvider()
    prediction_provider = MockPredictionProvider()
else:
    transit_provider = MockTransitProvider()
    safety_provider = MockSafetyProvider()
    prediction_provider = MockPredictionProvider()
