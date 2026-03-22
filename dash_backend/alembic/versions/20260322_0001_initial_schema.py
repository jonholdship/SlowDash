"""Initial schema (users, activities, activitystreams).

Revision ID: 20260322_0001
Revises:
Create Date: 2026-03-22

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260322_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("firstname", sa.String(), nullable=True),
        sa.Column("lastname", sa.String(), nullable=True),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "activities",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("distance", sa.Float(), nullable=True),
        sa.Column("moving_time", sa.Float(), nullable=True),
        sa.Column("elapsed_time", sa.Float(), nullable=True),
        sa.Column("total_elevation_gain", sa.Float(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("start_date_local", sa.DateTime(), nullable=True),
        sa.Column("location_city", sa.String(), nullable=True),
        sa.Column("location_country", sa.String(), nullable=True),
        sa.Column("kudos_count", sa.Integer(), nullable=True),
        sa.Column("athlete_count", sa.Integer(), nullable=True),
        sa.Column("gear_id", sa.String(), nullable=True),
        sa.Column("average_speed", sa.Float(), nullable=True),
        sa.Column("max_speed", sa.Float(), nullable=True),
        sa.Column("splits_metric", sa.Float(), nullable=True),
        sa.Column("splits_standard", sa.Float(), nullable=True),
        sa.Column("has_heartrate", sa.Boolean(), nullable=True),
        sa.Column("average_heartrate", sa.Float(), nullable=True),
        sa.Column("max_heartrate", sa.Float(), nullable=True),
        sa.Column("average_cadence", sa.Float(), nullable=True),
        sa.Column("device_name", sa.String(), nullable=True),
        sa.Column("calories", sa.Float(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("workout_type", sa.String(), nullable=True),
        sa.Column("pace", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "activitystreams",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=True),
        sa.Column("time", sa.Time(), nullable=True),
        sa.Column("distance", sa.Float(), nullable=True),
        sa.Column("heartrate", sa.Float(), nullable=True),
        sa.Column("cadence", sa.Float(), nullable=True),
        sa.Column("velocity_smooth", sa.Float(), nullable=True),
        sa.Column("pace", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("activitystreams")
    op.drop_table("activities")
    op.drop_table("users")
