from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user
from app.schemas.common import validate_city
from app.schemas.predictions import Prediction
from app.services.providers import prediction_provider

router = APIRouter(tags=["predictions"])


@router.get("/predictions/traffic", response_model=Prediction)
async def predictions(city: str = Query("delhi"), horizon: int = Query(15), user=Depends(get_current_user)) -> dict:
    if horizon not in (15, 30, 60):
        return {"horizon": horizon, "status": "unavailable", "current_traffic": 0, "predicted_traffic": 0, "drivers": [], "source": "MODEL_PLACEHOLDER"}
    return await prediction_provider.get_traffic_prediction(validate_city(city), horizon)
