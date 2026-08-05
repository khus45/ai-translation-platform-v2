"""Add auth fields to users

Revision ID: 9c1a2b3d4e5f
Revises: 7dd6d42167cb
Create Date: 2026-08-05 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "9c1a2b3d4e5f"
down_revision: Union[str, Sequence[str], None] = "7dd6d42167cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(length=50), nullable=False, server_default="user"),
    )
    op.add_column(
        "users",
        sa.Column("refresh_token_hash", sa.String(length=255), nullable=True),
    )
    op.alter_column("users", "role", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "refresh_token_hash")
    op.drop_column("users", "role")
