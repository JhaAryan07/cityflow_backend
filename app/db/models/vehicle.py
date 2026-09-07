import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class VehicleProfileModel(Base):
    __tablename__ = "vehicle_profiles"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    vehicle_type: Mapped[str] = mapped_column(String(30))
    height_m: Mapped[float] = mapped_column(Float)
    width_m: Mapped[float] = mapped_column(Float)
    length_m: Mapped[float] = mapped_column(Float)
    weight_t: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
