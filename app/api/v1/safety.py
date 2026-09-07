from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user
from app.schemas.common import validate_city
from app.services.providers import safety_provider

router = APIRouter(tags=["safety"])


@router.get("/safety")
async def safety(city: str = Query("delhi"), time_of_day: str = Query("evening", pattern="^(morning|afternoon|evening|night)$"), user=Depends(get_current_user)) -> dict:
    return await safety_provider.get_safety(validate_city(city), time_of_day)
