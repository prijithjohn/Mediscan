"""add created_at to alerts

Revision ID: add_alert_created_at
Revises: ca6882aa6344
Create Date: 2026-08-10 07:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_alert_created_at'
down_revision = 'ca6882aa6344'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('alerts', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE alerts SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"))
    with op.batch_alter_table('alerts') as batch_op:
        batch_op.alter_column('created_at', nullable=False)


def downgrade() -> None:
    op.drop_column('alerts', 'created_at')
