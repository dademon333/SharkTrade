"""Add items

Revision ID: 9b6fa951cc47
Revises: f68716778878
Create Date: 2022-06-03 19:16:01.292261

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '9b6fa951cc47'
down_revision = 'f68716778878'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_locked', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(('owner_id',), ['users.id'], name=op.f('fk_items_owner_id_users'), onupdate='CASCADE', ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_items'))
    )
    op.create_index(op.f('ix_items_owner_id'), 'items', ['owner_id'], unique=False)

    op.create_table(
        'item_photos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('media_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(('item_id',), ['items.id'], name=op.f('fk_item_photos_item_id_items'), onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(('media_id',), ['media.id'], name=op.f('fk_item_photos_media_id_media'), onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_item_photos'))
    )
    op.create_index(op.f('ix_item_photos_item_id'), 'item_photos', ['item_id'], unique=False)
    op.create_index(op.f('ix_item_photos_media_id'), 'item_photos', ['media_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_item_photos_media_id'), table_name='item_photos')
    op.drop_index(op.f('ix_item_photos_item_id'), table_name='item_photos')
    op.drop_table('item_photos')
    op.drop_index(op.f('ix_items_owner_id'), table_name='items')
    op.drop_table('items')
    # ### end Alembic commands ###
