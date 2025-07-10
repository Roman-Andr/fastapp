"""Roles

Revision ID: 62c41e1193bb
Revises: 730f426c24c9
Create Date: 2025-07-10 21:20:13.710174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '62c41e1193bb'
down_revision: Union[str, Sequence[str], None] = '730f426c24c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type with string values
    userrole_enum = sa.Enum('USER', 'MODERATOR', 'ADMIN', name='userrole')
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # Add the column with the enum type
    op.add_column('users', sa.Column(
        'role',
        userrole_enum,
        nullable=True,
        server_default='USER'
    ))

    # Set all existing rows to 'user' role
    op.execute("UPDATE users SET role = 'USER' WHERE role IS NULL")


def downgrade() -> None:
    """Downgrade schema."""
    # First drop the column
    op.drop_column('users', 'role')

    # Then drop the enum type
    userrole_enum = sa.Enum(name='userrole')
    userrole_enum.drop(op.get_bind(), checkfirst=True)