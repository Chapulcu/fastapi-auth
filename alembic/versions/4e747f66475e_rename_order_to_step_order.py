"""Rename order to step_order

Revision ID: 4e747f66475e
Revises: 3e747f66475e
Create Date: 2025-05-31 10:28:25.244113

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4e747f66475e'
down_revision: Union[str, None] = '3e747f66475e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite doesn't support ALTER TABLE RENAME COLUMN directly
    # We need to create a new table with the correct column name and copy the data
    
    # Create a new temporary table with the correct column name
    op.create_table('course_steps_new',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('step_order', sa.Integer(), nullable=False),  # Renamed from 'order'
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('subtitle', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_steps_new_id'), 'course_steps_new', ['id'], unique=False)
    
    # Copy data from the old table to the new table
    op.execute('INSERT INTO course_steps_new (id, course_id, step_order, title, subtitle, content, created_at, updated_at) '
               'SELECT id, course_id, "order", title, subtitle, content, created_at, updated_at FROM course_steps')
    
    # Drop the old table
    op.drop_table('course_steps')
    
    # Rename the new table to the original name
    op.rename_table('course_steps_new', 'course_steps')


def downgrade() -> None:
    # Reverse the process for downgrade
    op.create_table('course_steps_old',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),  # Original name
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('subtitle', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_steps_old_id'), 'course_steps_old', ['id'], unique=False)
    
    # Copy data from the current table to the old-style table
    op.execute('INSERT INTO course_steps_old (id, course_id, "order", title, subtitle, content, created_at, updated_at) '
               'SELECT id, course_id, step_order, title, subtitle, content, created_at, updated_at FROM course_steps')
    
    # Drop the current table
    op.drop_table('course_steps')
    
    # Rename the old-style table to the original name
    op.rename_table('course_steps_old', 'course_steps')