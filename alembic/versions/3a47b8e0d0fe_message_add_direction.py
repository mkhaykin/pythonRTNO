"""message add direction

Revision ID: 3a47b8e0d0fe
Revises: d2beb324d6eb
Create Date: 2024-05-29 21:17:13.205087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3a47b8e0d0fe'
down_revision: Union[str, None] = 'd2beb324d6eb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE directionenum AS ENUM ('IN', 'OUT', 'FORWARD');
    """)

    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('direction', postgresql.ENUM('IN', 'OUT', 'FORWARD', name='directionenum'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'direction')
    # ### end Alembic commands ###
