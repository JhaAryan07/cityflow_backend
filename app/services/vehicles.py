from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import VehicleProfileModel


async def list_user_vehicles(db: AsyncSession, user_id):
    return list((await db.execute(select(VehicleProfileModel).where(VehicleProfileModel.user_id == user_id).order_by(VehicleProfileModel.created_at))).scalars().all())
