"""custom field type

Revision ID: e60908d1ee3
Revises: 1d9702e91c2d
Create Date: 2014-11-25 17:07:40.509509

"""

# revision identifiers, used by Alembic.
revision = 'e60908d1ee3'
down_revision = '1d9702e91c2d'

from alembic import op
import sqlalchemy as sa
from mrt.models import CustomField


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'custom_field',
        sa.Column('custom_field_type', sa.Unicode(length=255),
                  nullable=False, server_default=CustomField.PARTICIPANT))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('custom_field', 'custom_field_type')
    ### end Alembic commands ###
