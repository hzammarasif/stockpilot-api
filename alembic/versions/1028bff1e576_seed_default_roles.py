"""seed default roles

Revision ID: 1028bff1e576
Revises: 1f0355bb5e5f
Create Date: 2026-07-19 20:43:47.197626
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "1028bff1e576"
down_revision: Union[str, Sequence[str], None] = "1f0355bb5e5f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


roles = sa.table(
    "roles",
    sa.column("id", sa.Integer),
    sa.column("name", sa.String),
    sa.column("description", sa.String),
)


def upgrade() -> None:
    op.bulk_insert(
        roles,
        [
            {
                "id": 1,
                "name": "admin",
                "description": "System Administrator",
            },
            {
                "id": 2,
                "name": "manager",
                "description": "Inventory Manager",
            },
            {
                "id": 3,
                "name": "employee",
                "description": "Inventory Employee",
            },
        ],
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            DELETE FROM roles
            WHERE id IN (1, 2, 3)
            """
        )
    )