"""component table

Revision ID: de4c96aa6ea5
Revises: 6d474cd60357
Create Date: 2024-11-18 20:51:27.943839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de4c96aa6ea5'
down_revision = '6d474cd60357'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('component',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('component_title', sa.String(length=70), nullable=False),
    sa.Column('component_body', sa.String(length=5000), nullable=False),
    sa.Column('component_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('component')
    # ### end Alembic commands ###