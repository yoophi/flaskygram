"""empty message

Revision ID: 5d46eced8fc3
Revises: 441964995962
Create Date: 2016-05-17 19:00:52.468806

"""

# revision identifiers, used by Alembic.
revision = '5d46eced8fc3'
down_revision = '441964995962'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('media', sa.Column('shortcode', sa.Unicode(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('media', 'shortcode')
    ### end Alembic commands ###
