"""Add sold field

Revision ID: 45278964bf98
Revises: 954b83bde719
Create Date: 2025-02-26 10:43:45.833450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45278964bf98'
down_revision: Union[str, None] = '954b83bde719'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('sold', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets', 'sold')
    # ### end Alembic commands ###
