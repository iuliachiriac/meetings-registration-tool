"""add registration date column

Revision ID: 31eaa9c4237d
Revises: c94e24a0df5
Create Date: 2016-07-22 12:01:16.567939

"""

# revision identifiers, used by Alembic.
revision = '31eaa9c4237d'
down_revision = 'c94e24a0df5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('participant', sa.Column('registration_date', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('participant', 'registration_date')
    ### end Alembic commands ###
