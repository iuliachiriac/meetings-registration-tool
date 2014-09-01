"""Added settings json on meeting

Revision ID: d4839030d26
Revises: 28ee7c8f487e
Create Date: 2014-08-29 14:40:05.200137

"""

# revision identifiers, used by Alembic.
revision = 'd4839030d26'
down_revision = '28ee7c8f487e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meeting', sa.Column('settings', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meeting', 'settings')
    ### end Alembic commands ###