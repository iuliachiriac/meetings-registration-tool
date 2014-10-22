"""Staff on ActiviyLog null

Revision ID: 29c64b2a9a6e
Revises: 57e914588132
Create Date: 2014-10-22 17:54:31.568939

"""

# revision identifiers, used by Alembic.
revision = '29c64b2a9a6e'
down_revision = '57e914588132'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('activity_log', 'staff_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('activity_log', 'staff_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    ### end Alembic commands ###
