import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SavedRouteModel(Base):
    __tablename__ = "saved_routes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    origin: Mapped[str] = mapped_column(String(255))
    destination: Mapped[str] = mapped_column(String(255))
    vehicle_profile_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("vehicle_profiles.id", ondelete="SET NULL"), nullable=True)
    preference: Mapped[str] = mapped_column(String(20), default="balanced")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
