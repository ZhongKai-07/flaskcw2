"""empty message

Revision ID: 583145881fd2
Revises: 8762a954f350
Create Date: 2021-11-30 21:52:59.350890

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '583145881fd2'
down_revision = '8762a954f350'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('body', sa.Text(), nullable=True))
    op.add_column('comment', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('comment', sa.Column('course_id', sa.Integer(), nullable=True))
    op.add_column('comment', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_comment_timestamp'), 'comment', ['timestamp'], unique=False)
    op.create_foreign_key(None, 'comment', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'comment', 'course', ['course_id'], ['id'])
    op.add_column('course', sa.Column('description', sa.Text(), nullable=True))
    op.drop_column('course', 'relation')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('course', sa.Column('relation', mysql.TEXT(), nullable=True))
    op.drop_column('course', 'description')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_index(op.f('ix_comment_timestamp'), table_name='comment')
    op.drop_column('comment', 'user_id')
    op.drop_column('comment', 'course_id')
    op.drop_column('comment', 'timestamp')
    op.drop_column('comment', 'body')
    # ### end Alembic commands ###