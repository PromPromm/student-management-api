"""empty message

Revision ID: 5b11cf6c4c3d
Revises: a40c4bb53e1e
Create Date: 2023-03-11 21:42:26.825042

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b11cf6c4c3d'
down_revision = 'a40c4bb53e1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('score', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score')
    # ### end Alembic commands ###