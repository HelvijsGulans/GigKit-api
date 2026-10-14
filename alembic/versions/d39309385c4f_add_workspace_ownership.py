"""add workspace ownership

Revision ID: d39309385c4f
Revises: ac8f944384c5
Create Date: 2026-10-14 16:50:19.401430

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "d39309385c4f"
down_revision: Union[str, Sequence[str], None] = "ac8f944384c5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "workspaces",
        sa.Column("owner_id", sa.Uuid(), nullable=False),
    )

    op.create_foreign_key(
        "fk_workspaces_owner_id_users",
        "workspaces",
        "users",
        ["owner_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_workspaces_owner_id_users",
        "workspaces",
        type_="foreignkey",
    )

    op.drop_column("workspaces", "owner_id")
