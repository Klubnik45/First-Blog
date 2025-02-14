"""create tables

Revision ID: 7add574378ff
Revises: 
Create Date: 2025-01-30 20:48:17.683318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7add574378ff'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('component',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('component_title', sa.String(length=70), nullable=False),
    sa.Column('component_body', sa.String(length=500), nullable=False),
    sa.Column('component_type', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=256), nullable=True),
    sa.Column('about_me', sa.String(length=256), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('question', sa.String(length=64), nullable=False),
    sa.Column('answer', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_answer'), ['answer'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_question'), ['question'], unique=False)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post_title', sa.String(length=70), nullable=False),
    sa.Column('post_body', sa.String(length=5000), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_post_date_created'), ['date_created'], unique=False)
        batch_op.create_index(batch_op.f('ix_post_user_id'), ['user_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_post_user_id'))
        batch_op.drop_index(batch_op.f('ix_post_date_created'))

    op.drop_table('post')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_question'))
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_index(batch_op.f('ix_user_answer'))

    op.drop_table('user')
    op.drop_table('component')
    # ### end Alembic commands ###
