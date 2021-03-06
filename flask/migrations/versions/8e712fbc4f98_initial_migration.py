"""Initial migration

Revision ID: 8e712fbc4f98
Revises: 
Create Date: 2021-06-05 17:24:04.194385

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8e712fbc4f98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_mark', sa.Enum('X', 'O', name='marktype'), nullable=False),
    sa.Column('result', sa.Enum('WIN', 'LOSE', 'DRAW', name='gameresulttype'), nullable=True),
    sa.Column('total_turns', sa.Integer(), nullable=True),
    sa.Column('overview', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('started_dttm', sa.DateTime(), nullable=False),
    sa.Column('finished_dttm', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    op.drop_table('users')
    # ### end Alembic commands ###
