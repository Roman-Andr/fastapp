"""User task connection

Revision ID: 730f426c24c9
Revises: 6146cf0fcd70
Create Date: 2025-07-10 18:55:34.893676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '730f426c24c9'
down_revision: Union[str, Sequence[str], None] = '6146cf0fcd70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'tasks', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'user_id')
    # ### end Alembic commands ###
