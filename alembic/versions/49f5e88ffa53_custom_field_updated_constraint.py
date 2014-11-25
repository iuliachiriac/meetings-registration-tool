"""custom field updated constraint

Revision ID: 49f5e88ffa53
Revises: e60908d1ee3
Create Date: 2014-11-25 17:33:27.080992

"""

# revision identifiers, used by Alembic.
revision = '49f5e88ffa53'
down_revision = 'e60908d1ee3'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'uq_custom_field', 'custom_field')
    # op.drop_index('uq_custom_field', table_name='custom_field')
    op.create_unique_constraint(None, 'custom_field', ['meeting_id', 'slug', 'custom_field_type'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'custom_field')
    # op.create_index('uq_custom_field', 'custom_field', ['meeting_id', 'slug'], unique=True)
    op.create_unique_constraint(u'uq_custom_field', 'custom_field', ['meeting_id', 'slug'])
    ### end Alembic commands ###
