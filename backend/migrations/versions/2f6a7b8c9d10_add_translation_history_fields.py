"""Add translation history fields

Revision ID: 2f6a7b8c9d10
Revises: 9c1a2b3d4e5f
Create Date: 2026-08-06 00:00:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "2f6a7b8c9d10"
down_revision: Union[str, Sequence[str], None] = "9c1a2b3d4e5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("translations", sa.Column("user_id", sa.Integer(), nullable=True))
    op.add_column(
        "translations",
        sa.Column(
            "provider", sa.String(length=50), nullable=False, server_default="local"
        ),
    )
    op.create_index(op.f("ix_translations_user_id"), "translations", ["user_id"])
    op.create_foreign_key(
        "fk_translations_user_id_users",
        "translations",
        "users",
        ["user_id"],
        ["id"],
    )
    op.alter_column("translations", "provider", server_default=None)


def downgrade() -> None:
    op.drop_constraint(
        "fk_translations_user_id_users", "translations", type_="foreignkey"
    )
    op.drop_index(op.f("ix_translations_user_id"), table_name="translations")
    op.drop_column("translations", "provider")
    op.drop_column("translations", "user_id")
