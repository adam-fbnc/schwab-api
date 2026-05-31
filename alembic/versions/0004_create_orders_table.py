"""create orders table

Revision ID: 0004
Revises: 0003
Create Date: 2026-05-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.String(), nullable=False),
        sa.Column("account_hash", sa.String(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=True),
        sa.Column("asset_type", sa.String(), nullable=True),
        sa.Column("order_type", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("quantity", sa.Numeric(precision=18, scale=6), nullable=True),
        sa.Column("price", sa.Numeric(precision=18, scale=6), nullable=True),
        sa.Column("entered_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("close_time", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw", JSONB(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("order_id"),
        sa.ForeignKeyConstraint(["account_hash"], ["accounts.account_hash"], ondelete="CASCADE"),
    )
    op.create_index("ix_orders_order_id", "orders", ["order_id"])
    op.create_index("ix_orders_account_hash", "orders", ["account_hash"])
    op.create_index("ix_orders_symbol", "orders", ["symbol"])
    op.create_index("ix_orders_status", "orders", ["status"])
    op.create_index("ix_orders_entered_time", "orders", ["entered_time"])


def downgrade() -> None:
    op.drop_index("ix_orders_entered_time", table_name="orders")
    op.drop_index("ix_orders_status", table_name="orders")
    op.drop_index("ix_orders_symbol", table_name="orders")
    op.drop_index("ix_orders_account_hash", table_name="orders")
    op.drop_index("ix_orders_order_id", table_name="orders")
    op.drop_table("orders")
