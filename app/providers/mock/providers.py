from typing import Any

from .data import city_data


class MockTrafficProvider:
    async def get_traffic(self, city: str) -> list[dict[str, Any]]:
        return city_data(city)["traffic"]


class MockIncidentProvider:
    async def get_incidents(self, city: str, page: int = 1, page_size: int = 100) -> dict[str, Any]:
        items = city_data(city)["incidents"]
        start = (page - 1) * page_size
        end = start + page_size
        return {"items": items[start:end], "page": page, "page_size": page_size, "total": len(items)}


class MockWeatherProvider:
    async def get_weather(self, city: str) -> dict[str, Any]:
        return city_data(city)["weather"]


class MockSafetyProvider:
    async def get_safety(self, city: str, time_of_day: str) -> dict[str, Any]:
        adjustment = {"morning": 2, "afternoon": 0, "evening": 5, "night": -4}.get(time_of_day, 0)
        items = []
        for risk in city_data(city)["risk"]:
            items.append({**risk, "score": max(0, min(100, risk["score"] + adjustment))})
        return {"city": city, "time_of_day": time_of_day, "source": "MODELLED_HISTORICAL", "hotspots": items}


class MockPredictionProvider:
    """Placeholder for the future ML service. This intentionally uses deterministic demo values."""

    async def get_traffic_prediction(self, city: str, horizon: int) -> dict[str, Any]:
        traffic = city_data(city)["traffic"]
        current = round(sum(x["current_speed"] for x in traffic) / max(1, len(traffic)), 1)
        deltas = {15: -3, 30: -6, 60: -2}
        predicted = max(0, current + deltas.get(horizon, 0))
        status = "likely stable" if horizon == 15 else "rising" if horizon == 30 else "heavy congestion"
        return {
            "horizon": horizon,
            "status": status,
            "current_traffic": current,
            "predicted_traffic": predicted,
            "drivers": ["Historical pattern", "Current network state", "Incidents", "Weather"],
            "source": "MODEL_PLACEHOLDER",
        }


class MockRoutingProvider:
    async def get_route(self, request: dict[str, Any]) -> list[dict[str, Any]]:
        vehicle = request["vehicle"]
        kind = vehicle["vehicle_type"]
        factor = {"Motorcycle": 0.07, "Car": 0.145, "Van": 0.19, "Bus": 0.38, "Truck": 0.48}[kind]
        restricted = vehicle["height_m"] > 3.5 or vehicle["weight_t"] > 10 or vehicle["width_m"] > 2.45
        base = {"Motorcycle": 25, "Car": 27, "Van": 30, "Bus": 32, "Truck": 34}[kind]
        fit = {"Motorcycle": 93, "Car": 88, "Van": 90, "Bus": 95, "Truck": 96}[kind]
        opts = [
            {"id": "a", "label": "Ring corridor", "geometry": [(28.596, 77.183), (28.614, 77.235), (28.638, 77.267)], "duration_min": base - 3, "distance_km": 14.9, "estimated_co2_kg": round(14.9 * factor, 1), "suitability_score": 58 if restricted else fit - 4, "restrictions": ["Height / weight restriction on one segment"] if restricted else [], "recommendation_reason": "Not suitable for selected dimensions" if restricted else "Fastest overall path"},
            {"id": "b", "label": "Vehicle-fit corridor", "geometry": [(28.575, 77.267), (28.592, 77.301), (28.604, 77.333)], "duration_min": base + 1, "distance_km": 16.2, "estimated_co2_kg": round(16.2 * factor * 0.83, 1), "suitability_score": fit, "restrictions": [], "recommendation_reason": "Best match for the selected vehicle"},
            {"id": "c", "label": "Lower-emission corridor", "geometry": [(28.552, 77.107), (28.568, 77.21), (28.63, 77.196)], "duration_min": base + 5, "distance_km": 17.1, "estimated_co2_kg": round(17.1 * factor * 0.68, 1), "suitability_score": max(75, fit - 3), "restrictions": [], "recommendation_reason": "Longer trip, lowest estimated emissions"},
        ]
        preference = request.get("preference", "balanced")
        key = {"emission": lambda x: x["estimated_co2_kg"], "fit": lambda x: -x["suitability_score"], "balanced": lambda x: x["duration_min"]}[preference]
        return sorted(opts, key=key)


class MockTransitProvider:
    async def get_network(self, city: str) -> dict[str, Any]:
        data = city_data(city)
        return {"city": city, **data["transit"], "airports": data["airports"]}

    async def plan_journey(self, request: dict[str, Any]) -> list[dict[str, Any]]:
        origin, destination, mode = request["origin"], request["destination"], request["mode"]
        base = [
            {"id": "j1", "mode": "metro", "duration": 42, "transfers": 1, "fare": 40, "label": "Metro + walk", "legs": [{"mode": "Metro", "line": "Yellow Line", "origin": origin, "destination": destination, "duration": 42, "stops": 15}], "geometry": [(28.644, 77.217), (28.63, 77.24), (28.592, 77.301)]},
            {"id": "j2", "mode": "mixed", "duration": 56, "transfers": 2, "fare": 35, "label": "Bus + Metro", "legs": [{"mode": "Bus", "line": "Route 740", "origin": origin, "destination": "ITO", "duration": 24, "stops": 10}, {"mode": "Metro", "line": "Blue Line", "origin": "ITO", "destination": destination, "duration": 32, "stops": 12}], "geometry": [(28.63, 77.196), (28.614, 77.235), (28.592, 77.301)]},
            {"id": "j3", "mode": "rail", "duration": 63, "transfers": 2, "fare": 55, "label": "Rail + Metro", "legs": [{"mode": "Rail", "line": "Regional Rail", "origin": origin, "destination": "Gurugram", "duration": 30, "stops": 4}, {"mode": "Metro", "line": "Yellow Line", "origin": "Gurugram", "destination": destination, "duration": 33, "stops": 11}], "geometry": [(28.596, 77.183), (28.614, 77.235), (28.592, 77.301)]},
            {"id": "j4", "mode": "bus", "duration": 56, "transfers": 2, "fare": 35, "label": "City bus", "legs": [{"mode": "Bus", "line": "Airport Feeder", "origin": origin, "destination": destination, "duration": 56, "stops": 21}], "geometry": [(28.63, 77.196), (28.614, 77.235), (28.592, 77.301)]},
        ]
        return [j for j in base if mode == "best" or j["mode"] == mode] or base
