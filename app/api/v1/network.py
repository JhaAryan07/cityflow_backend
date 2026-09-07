from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user
from app.schemas.common import validate_city
from app.schemas.network import NetworkResponse
from app.services.network import get_network

router = APIRouter(tags=["network"])

@router.get("/network", response_model=NetworkResponse)
async def network(city: str = Query("delhi"), user=Depends(get_current_user)) -> dict:
    return await get_network(validate_city(city))
