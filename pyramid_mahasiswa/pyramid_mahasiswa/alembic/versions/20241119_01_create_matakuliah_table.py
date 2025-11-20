"""Create matakuliah table

Revision ID: 20241119_01
Revises:
Create Date: 2025-11-19
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20241119_01'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'matakuliah',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('kode_mk', sa.Text(), nullable=False, unique=True),
        sa.Column('nama_mk', sa.Text(), nullable=False),
        sa.Column('sks', sa.Integer(), nullable=False),
        sa.Column('semester', sa.Integer(), nullable=False),
    )


def downgrade():
    op.drop_table('matakuliah')

