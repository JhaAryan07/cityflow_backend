from fastapi import APIRouter

from .health import router as health
from .incidents import router as incidents
from .network import router as network
from .predictions import router as predictions
from .routes import router as routes
from .safety import router as safety
from .transit import router as transit
from .users import router as users
from .vehicles import router as vehicles
from .weather import router as weather

router = APIRouter(prefix="/api/v1")
for route in (health, users, vehicles, routes, network, incidents, transit, weather, predictions, safety):
    router.include_router(route)
