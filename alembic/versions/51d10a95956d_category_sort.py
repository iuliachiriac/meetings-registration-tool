"""category sort

Revision ID: 51d10a95956d
Revises: 4560afdd7d4f
Create Date: 2014-07-25 12:47:53.758851

"""

# revision identifiers, used by Alembic.
revision = '51d10a95956d'
down_revision = '4560afdd7d4f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('sort', sa.Integer(), nullable=True))
    op.add_column('category_default', sa.Column('sort', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category_default', 'sort')
    op.drop_column('category', 'sort')
    ### end Alembic commands ###