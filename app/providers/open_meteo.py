from __future__ import annotations

from typing import Any

import httpx

from app.core.config import settings

DELHI_NCR_CENTER = (28.6139, 77.2090)

WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Drizzle",
    55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
    81: "Rain showers", 82: "Heavy rain showers", 95: "Thunderstorm",
    96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


class OpenMeteoProvider:
    async def _get(self, url: str, params: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()

    async def get_weather(self, city: str) -> dict[str, Any]:
        lat, lon = DELHI_NCR_CENTER
        weather, air = await self._get_both(lat, lon)
        current = weather.get("current", {})
        air_current = air.get("current", {})
        code = int(current.get("weather_code", -1))
        temp = float(current.get("temperature_2m", 0))
        rain = float(current.get("precipitation", 0))
        wind = float(current.get("wind_speed_10m", 0))
        aqi = int(round(float(air_current.get("us_aqi", 0))))
        adjustment = round(min(40.0, max(0.0, rain * 2 + max(0, aqi - 50) * 0.08)), 1)
        return {
            "temp": temp,
            "aqi": aqi,
            "rain": rain,
            "wind": wind,
            "condition": WEATHER_CODES.get(code, "Current conditions"),
            "adjustment": adjustment,
        }

    async def _get_both(self, lat: float, lon: float) -> tuple[dict[str, Any], dict[str, Any]]:
        weather_url = f"{settings.open_meteo_base_url.rstrip('/')}/forecast"
        air_url = f"{settings.open_meteo_aqi_base_url.rstrip('/')}/air-quality"
        params_w = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,precipitation,wind_speed_10m,weather_code",
            "timezone": "Asia/Kolkata",
        }
        params_a = {
            "latitude": lat,
            "longitude": lon,
            "current": "us_aqi,pm2_5,pm10",
            "timezone": "Asia/Kolkata",
        }
        async with httpx.AsyncClient(timeout=settings.request_timeout_seconds) as client:
            weather_resp, air_resp = await client.get(weather_url, params=params_w), await client.get(air_url, params=params_a)
        weather_resp.raise_for_status()
        air_resp.raise_for_status()
        return weather_resp.json(), air_resp.json()
