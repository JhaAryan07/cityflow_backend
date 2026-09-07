CITY_DATA = {
    "delhi": {
        "traffic": [
            {"id": "rr", "name": "Outer Ring Road", "coords": [(28.596, 77.183), (28.614, 77.235), (28.638, 77.267)], "current_speed": 21, "free_flow": 54, "level": "heavy"},
            {"id": "nh48", "name": "NH-48", "coords": [(28.552, 77.107), (28.535, 77.164), (28.568, 77.21)], "current_speed": 34, "free_flow": 58, "level": "moderate"},
        ],
        "incidents": [
            {"id": "i1", "type": "Accident", "road": "Outer Ring Road", "severity": "High", "minutes": 8, "impact": "Severe", "coords": (28.62, 77.235), "status": "ACTIVE"},
            {"id": "i2", "type": "Construction", "road": "NH-48", "severity": "Medium", "minutes": 24, "impact": "Moderate", "coords": (28.549, 77.157), "status": "ACTIVE"},
            {"id": "i3", "type": "Closure", "road": "DND Flyway", "severity": "High", "minutes": 35, "impact": "Severe", "coords": (28.592, 77.301), "status": "ACTIVE"},
            {"id": "i4", "type": "Obstruction", "road": "Ring Road", "severity": "Low", "minutes": 12, "impact": "Low", "coords": (28.635, 77.221), "status": "REPORTED"},
        ],
        "risk": [
            {"id": "r1", "name": "ITO Junction", "score": 82, "peak": "18:00–21:00", "count": 19, "coords": (28.628, 77.241), "factors": ["Evening traffic concentration", "Historic collision density", "Rain-sensitive approach roads"]},
            {"id": "r2", "name": "Ashram Interchange", "score": 74, "peak": "17:00–20:00", "count": 15, "coords": (28.576, 77.255), "factors": ["Merge conflict points", "Peak-hour congestion", "Frequent lane changes"]},
        ],
        "weather": {"temp": 29, "aqi": 112, "rain": 14, "wind": 11, "condition": "Hazy sunshine", "adjustment": 18},
        "transit": {
            "metro": [
                {"name": "Yellow Line", "color": "#f4c400", "stations": 37, "status": "Normal", "mode": "metro", "connections": ["Blue Line", "Violet Line"]},
                {"name": "Blue Line", "color": "#2473ff", "stations": 44, "status": "Normal", "mode": "metro", "connections": ["Yellow Line", "Red Line"]},
                {"name": "Red Line", "color": "#ef4b5f", "stations": 29, "status": "Minor delay", "mode": "metro", "connections": ["Blue Line"]},
                {"name": "Violet Line", "color": "#8f59dc", "stations": 32, "status": "Normal", "mode": "metro", "connections": ["Yellow Line"]},
            ],
            "bus": {"routes": 850, "stops": 8200},
            "rail": {"networks": 3, "stations": 42},
        },
        "airports": [
            {"name": "IGI Airport", "code": "DEL", "kind": "Passenger + Cargo", "connections": ["Airport Express", "Road corridor", "Freight access"]},
            {"name": "Jewar Airport", "code": "DXN", "kind": "Passenger + Cargo", "connections": ["Planned rapid transit", "Yamuna Expressway", "Freight corridor"]},
        ],
    },
    "mumbai": {
        "traffic": [{"id": "eeh", "name": "Eastern Express Highway", "coords": [(19.057, 72.91), (19.08, 72.94), (19.13, 72.96)], "current_speed": 27, "free_flow": 58, "level": "heavy"}],
        "incidents": [{"id": "m1", "type": "Accident", "road": "Western Express Highway", "severity": "High", "minutes": 11, "impact": "Severe", "coords": (19.11, 72.83), "status": "ACTIVE"}],
        "risk": [{"id": "mr1", "name": "Andheri Junction", "score": 86, "peak": "18:00–21:00", "count": 22, "coords": (19.12, 72.85), "factors": ["Evening traffic concentration", "Dense lane changes", "Historic collision density"]}],
        "weather": {"temp": 27, "aqi": 78, "rain": 9, "wind": 18, "condition": "Cloudy intervals", "adjustment": 12},
        "transit": {"metro": [{"name": "Line 1", "color": "#2c74ff", "stations": 12, "status": "Normal", "mode": "metro", "connections": ["Line 7"]}, {"name": "Line 2A", "color": "#f4c400", "stations": 17, "status": "Normal", "mode": "metro", "connections": ["Line 1"]}], "bus": {"routes": 570, "stops": 5200}, "rail": {"networks": 4, "stations": 83}},
        "airports": [{"name": "CSMIA", "code": "BOM", "kind": "Passenger + Cargo", "connections": ["Metro Line 3", "Road corridor", "Regional rail"]}],
    },
    "bengaluru": {
        "traffic": [{"id": "orr", "name": "Outer Ring Road", "coords": [(13.02, 77.61), (13.00, 77.66), (12.96, 77.69)], "current_speed": 23, "free_flow": 54, "level": "heavy"}],
        "incidents": [{"id": "b1", "type": "Obstruction", "road": "Outer Ring Road", "severity": "High", "minutes": 7, "impact": "Severe", "coords": (13.00, 77.66), "status": "ACTIVE"}],
        "risk": [{"id": "br1", "name": "Silk Board", "score": 91, "peak": "08:00–11:00", "count": 27, "coords": (12.917, 77.622), "factors": ["Extreme peak demand", "Merge conflicts", "Long queues"]}],
        "weather": {"temp": 24, "aqi": 64, "rain": 6, "wind": 9, "condition": "Partly cloudy", "adjustment": 8},
        "transit": {"metro": [{"name": "Purple Line", "color": "#7a4fd6", "stations": 37, "status": "Normal", "mode": "metro", "connections": ["Green Line"]}, {"name": "Green Line", "color": "#3cad67", "stations": 30, "status": "Normal", "mode": "metro", "connections": ["Purple Line"]}], "bus": {"routes": 700, "stops": 6900}, "rail": {"networks": 2, "stations": 26}},
        "airports": [{"name": "Kempegowda International", "code": "BLR", "kind": "Passenger + Cargo", "connections": ["Airport bus", "Road corridor", "Regional rail"]}],
    },
}


def city_data(city: str) -> dict:
    return CITY_DATA.get(city, CITY_DATA["delhi"])
