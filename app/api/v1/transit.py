from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user
from app.schemas.common import validate_city
from app.schemas.transit import Journey, JourneyRequest, TransitNetwork
from app.services.transit import get_network, plan_journey

router = APIRouter(tags=["transit"])

@router.get("/transit", response_model=TransitNetwork)
async def transit(city: str = Query("delhi"), user=Depends(get_current_user)) -> dict:
    return await get_network(validate_city(city))

@router.post("/transit/journey", response_model=list[Journey])
async def journey(payload: JourneyRequest, user=Depends(get_current_user)) -> list[dict]:
    return [dict(item, origin=payload.origin, destination=payload.destination) for item in await plan_journey(payload.model_dump())]
