import uuid

from fastapi import APIRouter, Depends, Query

from app.api.v1.deps import get_current_user, require_role
from app.schemas.common import validate_city
from app.schemas.incidents import IncidentCreate, IncidentResponse, IncidentStatusUpdate
from app.services.incidents import list_incidents

router = APIRouter(tags=["incidents"])

@router.get("/incidents")
async def incidents(city: str = Query("delhi"), page: int = Query(1, ge=1), page_size: int = Query(100, ge=1, le=200), user=Depends(get_current_user)) -> dict:
    return await list_incidents(validate_city(city), page, page_size)

@router.post("/incidents", response_model=IncidentResponse, status_code=201)
async def report_incident(payload: IncidentCreate, user=Depends(get_current_user)) -> IncidentResponse:
    return IncidentResponse(id=f"reported-{uuid.uuid4().hex[:8]}", status="REPORTED", **payload.model_dump())

@router.patch("/incidents/{incident_id}")
async def update_incident_status(incident_id: str, payload: IncidentStatusUpdate, user=Depends(require_role("AUTHORITY"))) -> dict:
    return {"id": incident_id, "status": payload.status, "updated_by": str(user["id"])}
