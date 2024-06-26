"""initial

Revision ID: 8a184c87bf05
Revises: 
Create Date: 2024-05-24 19:45:40.135180

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a184c87bf05'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
        CREATE FUNCTION public.refresh_updated_at()
        RETURNS TRIGGER
        LANGUAGE plpgsql NOT LEAKPROOF AS
        $BODY$
            BEGIN
               NEW.updated_at := now();
                RETURN NEW;
            END
        $BODY$;
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('drop function if exists refresh_updated_at;')
    # ### end Alembic commands ###
