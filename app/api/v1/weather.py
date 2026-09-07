from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user
from app.schemas.common import validate_city
from app.schemas.network import Weather
from app.services.providers import weather_provider

router = APIRouter(tags=["weather"])


@router.get("/weather", response_model=Weather)
async def weather(city: str = Query("delhi"), user=Depends(get_current_user)) -> dict:
    return await weather_provider.get_weather(validate_city(city))
