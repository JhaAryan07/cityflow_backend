from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.models import UserPreferenceModel, UserProfileModel
from app.db.session import get_db
from app.schemas.users import UserPreferenceUpdate, UserProfile

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserProfile)
async def me(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> UserProfileModel:
    profile = await db.get(UserProfileModel, user["id"])
    if profile is None:
        raise HTTPException(status_code=404, detail={"error": {"code": "USER_NOT_FOUND", "message": "User profile not found"}})
    return profile


@router.get("/preferences")
async def get_preferences(user=Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> UserPreferenceUpdate:
    row = await db.get(UserPreferenceModel, user["id"])
    if row is None:
        return UserPreferenceUpdate()
    return UserPreferenceUpdate.model_validate(row, from_attributes=True)


@router.put("/preferences", response_model=UserPreferenceUpdate)
async def update_preferences(payload: UserPreferenceUpdate, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)) -> UserPreferenceUpdate:
    if payload.default_vehicle_id is not None:
        from app.db.models import VehicleProfileModel
        vehicle = await db.get(VehicleProfileModel, payload.default_vehicle_id)
        if vehicle is None or vehicle.user_id != user["id"]:
            raise HTTPException(status_code=400, detail={"error": {"code": "INVALID_VEHICLE", "message": "Default vehicle does not belong to the current user"}})

    row = await db.get(UserPreferenceModel, user["id"])
    if row is None:
        row = UserPreferenceModel(user_id=user["id"], **payload.model_dump())
        db.add(row)
    else:
        row.default_vehicle_id = payload.default_vehicle_id
        row.preferred_route_type = payload.preferred_route_type
        row.units = payload.units
    await db.commit()
    return UserPreferenceUpdate.model_validate(row, from_attributes=True)
