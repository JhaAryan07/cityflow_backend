import asyncio
import uuid

from sqlalchemy import select

from app.db.base import Base
from app.db.models import UserPreferenceModel, UserProfileModel, VehicleProfileModel
from app.db.session import SessionLocal, engine


DEMO_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")

DEFAULT_VEHICLES = [
    ("Motorcycle", "Motorcycle", 1.3, 0.8, 2.2, 0.18),
    ("City Car", "Car", 1.7, 1.9, 4.5, 1.6),
    ("Delivery Van", "Van", 2.7, 2.1, 5.4, 2.8),
    ("City Bus", "Bus", 3.2, 2.5, 10.5, 10.0),
    ("Freight Truck", "Truck", 3.8, 2.5, 8.0, 12.0),
]


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as db:
        result = await db.execute(select(UserProfileModel).where(UserProfileModel.id == DEMO_USER_ID))
        user = result.scalar_one_or_none()
        if user is None:
            user = UserProfileModel(
                id=DEMO_USER_ID,
                auth_provider_user_id="mock:demo-user",
                name="CityFlow Demo",
                email="demo@cityflow.local",
                role="CITIZEN",
            )
            db.add(user)
            await db.flush()

        existing = await db.execute(select(VehicleProfileModel).where(VehicleProfileModel.user_id == DEMO_USER_ID))
        if not existing.scalars().first():
            for name, kind, height, width, length, weight in DEFAULT_VEHICLES:
                db.add(
                    VehicleProfileModel(
                        user_id=DEMO_USER_ID,
                        name=name,
                        vehicle_type=kind,
                        height_m=height,
                        width_m=width,
                        length_m=length,
                        weight_t=weight,
                    )
                )

        pref = await db.get(UserPreferenceModel, DEMO_USER_ID)
        if pref is None:
            db.add(UserPreferenceModel(user_id=DEMO_USER_ID, preferred_route_type="balanced", units="metric"))

        await db.commit()


if __name__ == "__main__":
    asyncio.run(init_db())
