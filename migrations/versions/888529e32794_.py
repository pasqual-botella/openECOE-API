"""empty message

Revision ID: 888529e32794
Revises: 
Create Date: 2018-05-02 08:10:45.453863

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '888529e32794'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('day',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_table('organization',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('stage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('duration', sa.Integer(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ecoe',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('shift',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.Enum('Mañana', 'Tarde', name='shifttype'), nullable=False),
    sa.Column('id_day', sa.Integer(), nullable=False),
    sa.Column('time_start', sa.String(length=5), nullable=True),
    sa.ForeignKeyConstraint(['id_day'], ['day.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code', 'id_day', name='shift_day_uk')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('surname', sa.String(length=255), nullable=True),
    sa.Column('is_superadmin', sa.Boolean(), nullable=False),
    sa.Column('token', sa.String(length=255), nullable=True),
    sa.Column('token_expiration', sa.DateTime(), nullable=True),
    sa.Column('id_organization', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_organization'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    op.create_table('area',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('ecoes_days',
    sa.Column('ecoe_id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['day_id'], ['day.id'], ),
    sa.ForeignKeyConstraint(['ecoe_id'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('ecoe_id', 'day_id')
    )
    op.create_table('station',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('wheel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('id_shift', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['id_shift'], ['shift.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code', 'id_shift', name='wheel_shift_uk')
    )
    op.create_table('qblock',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('id_station', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_station'], ['station.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('reference', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('id_area', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('RADIO_BUTTON', 'CHECK_BOX', name='qtype'), nullable=False),
    sa.ForeignKeyConstraint(['id_area'], ['area.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedule',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_ecoe', sa.Integer(), nullable=True),
    sa.Column('id_stage', sa.Integer(), nullable=False),
    sa.Column('id_station', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.ForeignKeyConstraint(['id_stage'], ['stage.id'], ),
    sa.ForeignKeyConstraint(['id_station'], ['station.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_ecoe', 'id_stage', name='ecoe_stage_uk'),
    sa.UniqueConstraint('id_station', 'id_stage', name='station_stage_uk')
    )
    op.create_table('student',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surnames', sa.String(length=100), nullable=False),
    sa.Column('dni', sa.String(length=10), nullable=True),
    sa.Column('id_ecoe', sa.Integer(), nullable=False),
    sa.Column('id_wheel', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_ecoe'], ['ecoe.id'], ),
    sa.ForeignKeyConstraint(['id_wheel'], ['wheel.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.Column('id_student', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_question'], ['question.id'], ),
    sa.ForeignKeyConstraint(['id_student'], ['student.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_question', 'id_student', name='question_student_uk')
    )
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('sound', sa.String(length=550), nullable=False),
    sa.Column('id_schedule', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_schedule'], ['schedule.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('id_question', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_question'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('qblocks_questions',
    sa.Column('qblock_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['qblock_id'], ['qblock.id'], ),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('qblock_id', 'question_id')
    )
    op.create_table('answers_options',
    sa.Column('answer_id', sa.Integer(), nullable=False),
    sa.Column('option_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['answer_id'], ['answer.id'], ),
    sa.ForeignKeyConstraint(['option_id'], ['option.id'], ),
    sa.PrimaryKeyConstraint('answer_id', 'option_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('answers_options')
    op.drop_table('qblocks_questions')
    op.drop_table('option')
    op.drop_table('event')
    op.drop_table('answer')
    op.drop_table('student')
    op.drop_table('schedule')
    op.drop_table('question')
    op.drop_table('qblock')
    op.drop_table('wheel')
    op.drop_table('station')
    op.drop_table('ecoes_days')
    op.drop_table('area')
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('shift')
    op.drop_table('ecoe')
    op.drop_table('stage')
    op.drop_table('organization')
    op.drop_table('day')
    # ### end Alembic commands ###
