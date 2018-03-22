"""empty message

Revision ID: a3dda3104e61
Revises: c61b9c992ba8
Create Date: 2018-03-22 08:26:11.725921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3dda3104e61'
down_revision = 'c61b9c992ba8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('org',
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id_organization')
    )
    op.create_table('ecoe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['org.id_organization'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('area',
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=257), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_area')
    )
    op.create_table('sta',
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_station')
    )
    op.create_table('stu',
    sa.Column('id_student', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('dni', sa.String(length=25), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id_student')
    )
    op.create_table('group',
    sa.Column('id_group', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_station'], ['sta.id_station'], ),
    sa.PrimaryKeyConstraint('id_group')
    )
    op.create_table('ques',
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.Column('id_group', sa.Integer(), nullable=False),
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('wording', sa.String(length=500), nullable=True),
    sa.Column('option_type', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['id_area'], ['area.id_area'], ),
    sa.ForeignKeyConstraint(['id_group'], ['group.id_group'], ),
    sa.PrimaryKeyConstraint('id_question')
    )
    op.create_table('opt',
    sa.Column('id_option', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_question'], ['ques.id_question'], ),
    sa.PrimaryKeyConstraint('id_option')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('opt')
    op.drop_table('ques')
    op.drop_table('group')
    op.drop_table('stu')
    op.drop_table('sta')
    op.drop_table('area')
    op.drop_table('ecoe')
    op.drop_table('org')
    # ### end Alembic commands ###
