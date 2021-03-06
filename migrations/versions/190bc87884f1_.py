"""empty message

Revision ID: 190bc87884f1
Revises: 5d46eced8fc3
Create Date: 2016-06-15 18:50:06.494631

"""

# revision identifiers, used by Alembic.
revision = '190bc87884f1'
down_revision = '5d46eced8fc3'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.add_column('media', sa.Column('image', sa.String(length=255), nullable=True))
    op.add_column('media', sa.Column('image_storage_bucket_name', sa.String(length=255), nullable=True))
    op.add_column('media', sa.Column('image_storage_type', sa.String(length=255), nullable=True))
    op.drop_constraint(u'media_post_id_fkey', 'media', type_='foreignkey')
    op.drop_column('media', 'mimetype')
    op.drop_column('media', 'name')
    op.drop_column('media', 'filename')
    op.drop_column('media', 'post_id')
    op.drop_column('media', 'filesize')
    op.drop_column('media', 'shortcode')
    op.drop_column('media', 'dir')
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('posts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('posts', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('posts', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.add_column('media', sa.Column('dir', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('media', sa.Column('shortcode', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('media', sa.Column('filesize', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('media', sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('media', sa.Column('filename', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('media', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('media', sa.Column('mimetype', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'media_post_id_fkey', 'media', 'posts', ['post_id'], ['id'])
    op.drop_column('media', 'image_storage_type')
    op.drop_column('media', 'image_storage_bucket_name')
    op.drop_column('media', 'image')
    op.create_table('tags',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name=u'tags_pkey')
    )
    ### end Alembic commands ###
