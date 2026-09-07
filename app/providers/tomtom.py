from __future__ import annotations

from typing import Any
from urllib.parse import quote

import httpx

from app.core.config import settings

DELHI_CORRIDORS = [
    ("Outer Ring Road", 28.6140, 77.2350),
    ("NH-48", 28.5490, 77.1570),
    ("DND Flyway", 28.5920, 77.3010),
    ("Ring Road", 28.6350, 77.2210),
    ("ITO", 28.6280, 77.2410),
]


class TomTomError(RuntimeError):
    pass


class TomTomClient:
    def __init__(self) -> None:
        self.base_url = settings.tomtom_base_url.rstrip("/")
        self.timeout = settings.request_timeout_seconds
        self.api_key = settings.tomtom_api_key

    def _require_key(self) -> str:
        if not self.api_key:
            raise TomTomError("TOMTOM_API_KEY is not configured")
        return self.api_key

    async def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        params = {**params, "key": self._require_key()}
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}{path}", params=params)
        if response.is_error:
            raise TomTomError(f"TomTom request failed: HTTP {response.status_code}")
        return response.json()

    async def flow(self, latitude: float, longitude: float) -> dict[str, Any]:
        return await self._get(
            "/traffic/services/4/flowSegmentData/absolute/10/json",
            {"point": f"{latitude},{longitude}", "unit": "KMPH"},
        )

    async def route(self, origin: tuple[float, float], destination: tuple[float, float]) -> dict[str, Any]:
        path = f"/routing/1/calculateRoute/{origin[0]},{origin[1]}:{destination[0]},{destination[1]}/json"
        return await self._get(path, {"traffic": "true", "routeType": "fastest", "computeBestOrder": "false"})

    async def incidents(self, bbox: tuple[float, float, float, float]) -> dict[str, Any]:
        min_lon, min_lat, max_lon, max_lat = bbox
        bbox_text = f"{min_lat},{min_lon},{max_lat},{max_lon}"
        # TomTom Traffic Incident Details API.
        return await self._get(
            f"/traffic/services/5/incidentDetails/s3/10/{bbox_text}/json",
            {},
        )


def _traffic_level(current: float, free_flow: float) -> str:
    ratio = current / max(free_flow, 1.0)
    if ratio >= 0.70:
        return "light"
    if ratio >= 0.45:
        return "moderate"
    return "heavy"


class TomTomTrafficProvider:
    async def get_traffic(self, city: str) -> list[dict[str, Any]]:
        client = TomTomClient()
        results: list[dict[str, Any]] = []
        for name, lat, lon in DELHI_CORRIDORS:
            data = await client.flow(lat, lon)
            flow = data.get("flowSegmentData", data)
            current = float(flow.get("currentSpeed", 0))
            free_flow = float(flow.get("freeFlowSpeed", max(current, 1)))
            coords = []
            for point in flow.get("coordinates", {}).get("coordinate", []):
                if "latitude" in point and "longitude" in point:
                    coords.append((float(point["latitude"]), float(point["longitude"])))
            if len(coords) < 2:
                coords = [(lat, lon)]
            results.append(
                {
                    "id": name.lower().replace(" ", "-")[:24],
                    "name": name,
                    "coords": coords,
                    "current_speed": current,
                    "free_flow": free_flow,
                    "level": _traffic_level(current, free_flow),
                }
            )
        return results


class TomTomRoutingProvider:
    async def get_route(self, request: dict[str, Any]) -> list[dict[str, Any]]:
        origin = await _geocode_text(request["origin"])
        destination = await _geocode_text(request["destination"])
        client = TomTomClient()
        data = await client.route(origin, destination)
        routes = data.get("routes", [])
        if not routes:
            raise TomTomError("TomTom returned no route")

        vehicle = request["vehicle"]
        preference = request.get("preference", "balanced")
        emission_factor = {"Motorcycle": 0.07, "Car": 0.145, "Van": 0.19, "Bus": 0.38, "Truck": 0.48}[vehicle["vehicle_type"]]
        output: list[dict[str, Any]] = []
        for index, route in enumerate(routes[:3]):
            summary = route.get("summary", {})
            length_km = float(summary.get("lengthInMeters", 0)) / 1000
            duration_min = max(1, round(float(summary.get("travelTimeInSeconds", 0)) / 60))
            geometry: list[tuple[float, float]] = []
            for point in route.get("legs", [{}])[0].get("points", []):
                if "latitude" in point and "longitude" in point:
                    geometry.append((float(point["latitude"]), float(point["longitude"])))
            if not geometry:
                geometry = [origin, destination]
            co2 = round(length_km * emission_factor, 1)
            suitability = 92
            restrictions: list[str] = []
            if vehicle["height_m"] > 3.5:
                restrictions.append("Verify bridge clearance")
                suitability -= 4
            if vehicle["weight_t"] > 10:
                restrictions.append("Verify heavy-vehicle restriction")
                suitability -= 4
            output.append(
                {
                    "id": f"tomtom-{index + 1}",
                    "label": "Live traffic route" if index == 0 else f"Alternative route {index}",
                    "geometry": geometry,
                    "duration_min": duration_min,
                    "distance_km": round(length_km, 1),
                    "estimated_co2_kg": co2,
                    "suitability_score": max(0, suitability),
                    "restrictions": restrictions,
                    "recommendation_reason": {
                        "balanced": "Best live-time balance of travel time and suitability",
                        "fit": "Best available route for the selected vehicle profile",
                        "emission": "Lowest estimated emissions among returned routes",
                    }[preference],
                }
            )
        key = {
            "balanced": lambda x: (x["duration_min"], -x["suitability_score"]),
            "fit": lambda x: (-x["suitability_score"], x["duration_min"]),
            "emission": lambda x: (x["estimated_co2_kg"], x["duration_min"]),
        }[preference]
        return sorted(output, key=key)


async def _geocode_text(value: str) -> tuple[float, float]:
    text = value.strip()
    parts = [part.strip() for part in text.split(",")]
    if len(parts) == 2:
        try:
            return float(parts[0]), float(parts[1])
        except ValueError:
            pass

    # TomTom Search API. Keep the geocoder inside the backend so the API key never reaches the browser.
    client = TomTomClient()
    encoded = quote(text, safe="")
    data = await client._get(
        f"/search/2/search/{encoded}.json",
        {"limit": 1, "countrySet": "IN"},
    )
    results = data.get("results", [])
    if not results:
        raise TomTomError(f"Could not geocode '{value}'")
    position = results[0].get("position", {})
    lat = float(position["lat"])
    lon = float(position["lon"])
    if not (settings.delhi_lat_min <= lat <= settings.delhi_lat_max and settings.delhi_lon_min <= lon <= settings.delhi_lon_max):
        raise TomTomError("Origin/destination must be inside the Delhi NCR operating region")
    return lat, lon


class TomTomIncidentProvider:
    async def get_incidents(self, city: str, page: int = 1, page_size: int = 100) -> dict[str, Any]:
        client = TomTomClient()
        data = await client.incidents((settings.delhi_lon_min, settings.delhi_lat_min, settings.delhi_lon_max, settings.delhi_lat_max))
        raw = data.get("incidents", [])
        items: list[dict[str, Any]] = []
        for i, incident in enumerate(raw):
            props = incident.get("properties", incident)
            geometry = incident.get("geometry", {})
            coords = geometry.get("coordinates", [None, None])
            # TomTom may provide either a point or a line; use the first point for the dashboard marker.
            if coords and isinstance(coords[0], list):
                coords = coords[0]
            if len(coords) < 2 or coords[0] is None or coords[1] is None:
                continue
            severity = str(props.get("magnitudeOfDelay", props.get("severity", "Medium"))).lower()
            sev = "High" if severity in {"high", "major", "severe", "4", "3"} else "Low" if severity in {"low", "minor", "1"} else "Medium"
            items.append(
                {
                    "id": str(props.get("id", f"tomtom-{i}")),
                    "type": props.get("events", [{}])[0].get("description", "Traffic incident") if isinstance(props.get("events"), list) and props.get("events") else props.get("iconCategory", "Traffic incident"),
                    "road": props.get("from", "Delhi NCR corridor"),
                    "severity": sev,
                    "minutes": max(0, round(float(props.get("delay", 0)) / 60)),
                    "impact": props.get("delay", 0) and "Severe" if sev == "High" else "Moderate" if sev == "Medium" else "Low",
                    "coords": (float(coords[1]), float(coords[0])),
                    "status": "ACTIVE",
                }
            )
        start = (page - 1) * page_size
        return {"items": items[start : start + page_size], "page": page, "page_size": page_size, "total": len(items)}
