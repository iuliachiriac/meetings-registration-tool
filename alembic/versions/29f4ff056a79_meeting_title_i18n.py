"""meeting title i18n

Revision ID: 29f4ff056a79
Revises: 220f4a6c2d73
Create Date: 2014-07-15 12:34:39.086715

"""

# revision identifiers, used by Alembic.
revision = '29f4ff056a79'
down_revision = '220f4a6c2d73'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meeting', sa.Column('title_id', sa.Integer(), nullable=False))
    op.drop_column('meeting', 'title')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meeting', sa.Column('title', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.drop_column('meeting', 'title_id')
    ### end Alembic commands ###