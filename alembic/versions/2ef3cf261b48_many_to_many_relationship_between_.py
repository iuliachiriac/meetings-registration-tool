"""many-to-many relationship between category_default and meeting_type

Revision ID: 2ef3cf261b48
Revises: 394553a02af1
Create Date: 2014-12-23 05:28:07.820757

"""

# revision identifiers, used by Alembic.
revision = '2ef3cf261b48'
down_revision = '394553a02af1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('meeting_type_default_category',
    sa.Column('meeting_type_slug', sa.String(length=16), nullable=True),
    sa.Column('category_default_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_default_id'], ['category_default.id'], ),
    sa.ForeignKeyConstraint(['meeting_type_slug'], ['meeting_type.slug'], )
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('meeting_type_default_category')
    ### end Alembic commands ###
