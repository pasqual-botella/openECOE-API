"""empty message

Revision ID: 6f07938182e5
Revises: 0c804508a5f5
Create Date: 2018-03-07 12:04:54.911420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f07938182e5'
down_revision = '0c804508a5f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('day', sa.Column('date', sa.Date(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('day', 'date')
    # ### end Alembic commands ###
