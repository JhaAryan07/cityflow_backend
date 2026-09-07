import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.errors import not_found
from app.db.models import SavedRouteModel, VehicleProfileModel
from app.db.session import get_db
from app.schemas.routes import RouteOption, SavedRoute, SavedRouteCreate, VehicleRouteRequest
from app.services.routes import get_vehicle_routes

router = APIRouter(tags=["routes"])

@router.post("/routes/vehicle", response_model=list[RouteOption])
async def vehicle_route(payload: VehicleRouteRequest, user=Depends(get_current_user)) -> list[dict]:
    return await get_vehicle_routes(payload.model_dump())

@router.get("/routes/saved", response_model=list[SavedRoute])
async def saved_routes(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> list[SavedRouteModel]:
    rows = (await db.execute(select(SavedRouteModel).where(SavedRouteModel.user_id == user["id"]).order_by(SavedRouteModel.created_at.desc()))).scalars().all()
    return list(rows)

@router.post("/routes/saved", response_model=SavedRoute, status_code=201)
async def create_saved_route(payload: SavedRouteCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> SavedRouteModel:
    if payload.vehicle_profile_id is not None:
        vehicle = await db.get(VehicleProfileModel, payload.vehicle_profile_id)
        if vehicle is None or vehicle.user_id != user["id"]:
            raise not_found("VEHICLE_NOT_FOUND", "Vehicle profile not found")
    row = SavedRouteModel(id=uuid.uuid4(), user_id=user["id"], **payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row

@router.delete("/routes/saved/{route_id}")
async def delete_saved_route(route_id: uuid.UUID, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> dict[str, bool]:
    row = await db.get(SavedRouteModel, route_id)
    if row is None or row.user_id != user["id"]:
        raise not_found("SAVED_ROUTE_NOT_FOUND", "Saved route not found")
    await db.delete(row)
    await db.commit()
    return {"deleted": True}
