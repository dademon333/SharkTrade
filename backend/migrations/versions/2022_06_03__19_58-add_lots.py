"""Add lots

Revision ID: 7d164c67dc55
Revises: 9b6fa951cc47
Create Date: 2022-06-03 19:58:36.041808

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '7d164c67dc55'
down_revision = '9b6fa951cc47'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'lots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('item_id', sa.Integer(), nullable=True),
        sa.Column('is_canceled', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('is_withdrawn', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('win_bid_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('end_time', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(('item_id',), ['items.id'], name=op.f('fk_lots_item_id_items'), onupdate='CASCADE', ondelete='SET NULL'),
        sa.ForeignKeyConstraint(('owner_id',), ['users.id'], name=op.f('fk_lots_owner_id_users'), onupdate='CASCADE', ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_lots'))
    )
    op.create_index(op.f('ix_lots_item_id'), 'lots', ['item_id'], unique=False)
    op.create_index(op.f('ix_lots_owner_id'), 'lots', ['owner_id'], unique=False)
    op.create_index(op.f('ix_lots_win_bid_id'), 'lots', ['win_bid_id'], unique=False)

    op.create_table(
        'bids',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('lot_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('is_withdrawn', sa.Boolean(), server_default='false', nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(('lot_id',), ['lots.id'], name=op.f('fk_bids_lot_id_lots'), onupdate='CASCADE', ondelete='SET NULL'),
        sa.ForeignKeyConstraint(('owner_id',), ['users.id'], name=op.f('fk_bids_owner_id_users'), onupdate='CASCADE', ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_bids'))
    )
    op.create_index(op.f('ix_bids_lot_id'), 'bids', ['lot_id'], unique=False)
    op.create_index(op.f('ix_bids_owner_id'), 'bids', ['owner_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_bids_owner_id'), table_name='bids')
    op.drop_index(op.f('ix_bids_lot_id'), table_name='bids')
    op.drop_table('bids')
    op.drop_index(op.f('ix_lots_win_bid_id'), table_name='lots')
    op.drop_index(op.f('ix_lots_owner_id'), table_name='lots')
    op.drop_index(op.f('ix_lots_item_id'), table_name='lots')
    op.drop_table('lots')
    # ### end Alembic commands ###
