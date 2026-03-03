"""add content column to posts table

Revision ID: 0b6115ca005e
Revises: b56a3adbe7d8
Create Date: 2026-02-26 12:55:26.900817

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0b6115ca005e"
down_revision: Union[str, Sequence[str], None] = "b56a3adbe7d8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
