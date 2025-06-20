"""Add users table and user_id to contacts

Revision ID: add_users_table
Revises: 4ec3399ca615
Create Date: 2025-06-20 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_users_table'
down_revision: Union[str, None] = '4ec3399ca615'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('avatar', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    
    # Create a default user for existing contacts
    op.execute("""
        INSERT INTO users (username, email, hashed_password, is_active, is_verified)
        VALUES ('admin', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj5i4qDx.QHO', true, true)
    """)
    
    # Add user_id column to contacts table
    op.add_column('contacts', sa.Column('user_id', sa.Integer(), nullable=True))
    
    # Set all existing contacts to belong to the default user (id=1)
    op.execute("UPDATE contacts SET user_id = 1 WHERE user_id IS NULL")
    
    # Now make user_id not nullable and add foreign key
    op.alter_column('contacts', 'user_id', nullable=False)
    op.create_foreign_key('fk_contacts_user_id', 'contacts', 'users', ['user_id'], ['id'])


def downgrade() -> None:
    # Remove user_id column from contacts table
    op.drop_constraint('fk_contacts_user_id', 'contacts', type_='foreignkey')
    op.drop_column('contacts', 'user_id')
    
    # Drop users table
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')