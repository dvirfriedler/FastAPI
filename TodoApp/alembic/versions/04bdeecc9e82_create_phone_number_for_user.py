"""Create phone number for user

Revision ID: 04bdeecc9e82
Revises: 
Create Date: 2024-05-10 10:46:19.398987

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04bdeecc9e82'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(255), nullable=True))


def downgrade() -> None:
    pass
