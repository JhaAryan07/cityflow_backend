from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import UserProfileModel
from app.services.auth import DEMO_USER


async def get_demo_profile(db: AsyncSession) -> UserProfileModel | None:
    return await db.get(UserProfileModel, DEMO_USER["id"])
