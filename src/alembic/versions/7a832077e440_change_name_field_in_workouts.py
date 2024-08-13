"""change name field in workouts

Revision ID: 7a832077e440
Revises: 9d341a9ce190
Create Date: 2024-08-13 23:15:05.541491

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a832077e440'
down_revision: Union[str, None] = '9d341a9ce190'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_workouts_name', table_name='workouts')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_workouts_name', 'workouts', ['name'], unique=True)
    # ### end Alembic commands ###
