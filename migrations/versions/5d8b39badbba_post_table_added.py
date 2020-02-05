"""post table added

Revision ID: 5d8b39badbba
Revises: 40ecd0446cbb
Create Date: 2020-01-09 22:56:20.334344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d8b39badbba'
down_revision = '40ecd0446cbb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=200), nullable=True),
    sa.Column('timeStamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timeStamp'), 'post', ['timeStamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_timeStamp'), table_name='post')
    op.drop_table('post')
    # ### end Alembic commands ###