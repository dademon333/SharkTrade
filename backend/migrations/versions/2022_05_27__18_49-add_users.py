"""Add users

Revision ID: 6f435f96e9ed
Revises:
Create Date: 2022-05-27 18:49:38.203665

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.

revision = '6f435f96e9ed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('user', 'admin', name='user_status'), nullable=False, server_default='user'),
        sa.Column('rubles_balance', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('rubles_balance >= 0', name=op.f('ck_users_rubles_balance')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    # ### end Alembic commands ###
    op.create_index(op.f('ix_users_email'), 'users', [sa.text('LOWER(email)')], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', [sa.text('LOWER(username)')], unique=True)


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
    ENUM(name='user_status').drop(op.get_bind(), checkfirst=False)
