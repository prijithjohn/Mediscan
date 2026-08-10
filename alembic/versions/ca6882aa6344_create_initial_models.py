"""create initial models
Revision ID: ca6882aa6344
Revises: 
Create Date: 2026-08-08 14:24:03.151798
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca6882aa6344'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('username', sa.String(length=128), nullable=False),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('password_hash', sa.String(length=256), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_username', 'users', ['username'], unique=False)
    op.create_index('ix_users_email', 'users', ['email'], unique=False)

    op.create_table(
        'prescriptions',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('original_text', sa.Text(), nullable=True),
        sa.Column('summary', sa.Text(), nullable=True),
        sa.Column('medicines', sa.JSON(), nullable=True),
        sa.Column('dosage', sa.String(length=256), nullable=True),
        sa.Column('frequency', sa.String(length=256), nullable=True),
        sa.Column('duration', sa.String(length=256), nullable=True),
        sa.Column('possible_conditions', sa.JSON(), nullable=True),
        sa.Column('warnings', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index('ix_prescriptions_id', 'prescriptions', ['id'], unique=False)

    op.create_table(
        'subscriptions',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('plan', sa.String(length=128), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.sql.expression.true()),
        sa.Column('started_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_subscriptions_id', 'subscriptions', ['id'], unique=False)

    op.create_table(
        'usages',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('usage_date', sa.Date(), nullable=False),
        sa.Column('used_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('usage_limit', sa.Integer(), nullable=False, server_default='10'),
    )
    op.create_index('ix_usages_id', 'usages', ['id'], unique=False)

    op.create_table(
        'alerts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('prescription_id', sa.Integer(), sa.ForeignKey('prescriptions.id', ondelete='SET NULL'), nullable=True),
        sa.Column('email', sa.String(length=256), nullable=False),
        sa.Column('subject', sa.String(length=256), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('status', sa.String(length=64), nullable=False, server_default='PENDING'),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index('ix_alerts_id', 'alerts', ['id'], unique=False)


def downgrade() -> None:
    op.drop_table('alerts')
    op.drop_table('usages')
    op.drop_table('subscriptions')
    op.drop_table('prescriptions')
    op.drop_table('users')
