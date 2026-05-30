"""create transactions table

Revision ID: 0005
Revises: 0004
Create Date: 2026-05-29
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("transaction_id", sa.String(), nullable=False),
        sa.Column("account_hash", sa.String(), nullable=False),
        sa.Column("transaction_type", sa.String(), nullable=True),
        sa.Column("symbol", sa.String(), nullable=True),
        sa.Column("cusip", sa.String(), nullable=True),
        sa.Column("amount", sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column("fees", sa.Numeric(precision=18, scale=4), nullable=True),
        sa.Column("trade_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("settlement_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("raw", JSONB(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("transaction_id"),
        sa.ForeignKeyConstraint(["account_hash"], ["accounts.account_hash"], ondelete="CASCADE"),
    )
    op.create_index("ix_transactions_transaction_id", "transactions", ["transaction_id"])
    op.create_index("ix_transactions_account_hash", "transactions", ["account_hash"])
    op.create_index("ix_transactions_symbol", "transactions", ["symbol"])
    op.create_index("ix_transactions_cusip", "transactions", ["cusip"])
    op.create_index("ix_transactions_type", "transactions", ["transaction_type"])
    op.create_index("ix_transactions_trade_date", "transactions", ["trade_date"])


def downgrade() -> None:
    op.drop_index("ix_transactions_trade_date", table_name="transactions")
    op.drop_index("ix_transactions_type", table_name="transactions")
    op.drop_index("ix_transactions_cusip", table_name="transactions")
    op.drop_index("ix_transactions_symbol", table_name="transactions")
    op.drop_index("ix_transactions_account_hash", table_name="transactions")
    op.drop_index("ix_transactions_transaction_id", table_name="transactions")
    op.drop_table("transactions")
