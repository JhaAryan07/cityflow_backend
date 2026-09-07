import uuid

from sqlalchemy import ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class UserPreferenceModel(Base):
    __tablename__ = "user_preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("user_profiles.id", ondelete="CASCADE"), primary_key=True)
    default_vehicle_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("vehicle_profiles.id", ondelete="SET NULL"), nullable=True)
    preferred_route_type: Mapped[str] = mapped_column(String(20), default="balanced")
    units: Mapped[str] = mapped_column(String(20), default="metric")
