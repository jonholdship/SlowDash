"""Add user HR zone fields (birthday, max_hr_override, hr_zone_highlight).

Revision ID: 20260328_0002
Revises: 20260322_0001
Create Date: 2026-03-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "20260328_0002"
down_revision: Union[str, Sequence[str], None] = "20260322_0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("birthday", sa.Date(), nullable=True))
    op.add_column("users", sa.Column("max_hr_override", sa.Float(), nullable=True))
    op.add_column(
        "users",
        sa.Column("hr_zone_highlight", sa.SmallInteger(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "hr_zone_highlight")
    op.drop_column("users", "max_hr_override")
    op.drop_column("users", "birthday")
