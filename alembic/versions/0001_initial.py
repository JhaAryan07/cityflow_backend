"""initial CityFlow persistence tables

Revision ID: 0001_initial
Revises:
Create Date: 2026-09-05
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("auth_provider_user_id", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column("role", sa.String(length=32), nullable=False, server_default="CITIZEN"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("auth_provider_user_id"),
    )
    op.create_index("ix_user_profiles_auth_provider_user_id", "user_profiles", ["auth_provider_user_id"], unique=False)
    op.create_index("ix_user_profiles_email", "user_profiles", ["email"], unique=False)

    op.create_table(
        "vehicle_profiles",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("vehicle_type", sa.String(length=30), nullable=False),
        sa.Column("height_m", sa.Float(), nullable=False),
        sa.Column("width_m", sa.Float(), nullable=False),
        sa.Column("length_m", sa.Float(), nullable=False),
        sa.Column("weight_t", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_vehicle_profiles_user_id", "vehicle_profiles", ["user_id"], unique=False)

    op.create_table(
        "saved_routes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("origin", sa.String(length=255), nullable=False),
        sa.Column("destination", sa.String(length=255), nullable=False),
        sa.Column("vehicle_profile_id", sa.Uuid(), nullable=True),
        sa.Column("preference", sa.String(length=20), nullable=False, server_default="balanced"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user_profiles.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vehicle_profile_id"], ["vehicle_profiles.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_saved_routes_user_id", "saved_routes", ["user_id"], unique=False)

    op.create_table(
        "user_preferences",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("default_vehicle_id", sa.Uuid(), nullable=True),
        sa.Column("preferred_route_type", sa.String(length=20), nullable=False, server_default="balanced"),
        sa.Column("units", sa.String(length=20), nullable=False, server_default="metric"),
        sa.ForeignKeyConstraint(["default_vehicle_id"], ["vehicle_profiles.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["user_profiles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id"),
    )


def downgrade() -> None:
    op.drop_table("user_preferences")
    op.drop_index("ix_saved_routes_user_id", table_name="saved_routes")
    op.drop_table("saved_routes")
    op.drop_index("ix_vehicle_profiles_user_id", table_name="vehicle_profiles")
    op.drop_table("vehicle_profiles")
    op.drop_index("ix_user_profiles_email", table_name="user_profiles")
    op.drop_index("ix_user_profiles_auth_provider_user_id", table_name="user_profiles")
    op.drop_table("user_profiles")
