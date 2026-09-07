import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.core.errors import not_found
from app.db.models import VehicleProfileModel
from app.db.session import get_db
from app.schemas.vehicles import Vehicle, VehicleCreate, VehicleUpdate

router = APIRouter(tags=["vehicles"])


@router.get("/vehicles", response_model=list[Vehicle])
async def list_vehicles(db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> list[VehicleProfileModel]:
    rows = (await db.execute(select(VehicleProfileModel).where(VehicleProfileModel.user_id == user["id"]).order_by(VehicleProfileModel.created_at))).scalars().all()
    return list(rows)


@router.post("/vehicles", response_model=Vehicle, status_code=201)
async def create_vehicle(payload: VehicleCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> VehicleProfileModel:
    row = VehicleProfileModel(id=uuid.uuid4(), user_id=user["id"], **payload.model_dump())
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


@router.patch("/vehicles/{vehicle_id}", response_model=Vehicle)
async def update_vehicle(vehicle_id: uuid.UUID, payload: VehicleUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> VehicleProfileModel:
    row = await db.get(VehicleProfileModel, vehicle_id)
    if row is None or row.user_id != user["id"]:
        raise not_found("VEHICLE_NOT_FOUND", "Vehicle profile not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(row, key, value)
    await db.commit()
    await db.refresh(row)
    return row


@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: uuid.UUID, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)) -> dict[str, bool]:
    row = await db.get(VehicleProfileModel, vehicle_id)
    if row is None or row.user_id != user["id"]:
        raise not_found("VEHICLE_NOT_FOUND", "Vehicle profile not found")
    await db.delete(row)
    await db.commit()
    return {"deleted": True}
