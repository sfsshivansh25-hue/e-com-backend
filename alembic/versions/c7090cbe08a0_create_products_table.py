"""create products table

Revision ID: c7090cbe08a0
Revises: 
Create Date: 2026-01-28
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c7090cbe08a0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.CheckConstraint("price > 0", name="price_positive"),
        sa.CheckConstraint("stock >= 0", name="stock_non_negative"),
    )
    op.create_index("ix_products_name", "products", ["name"])


def downgrade():
    op.drop_index("ix_products_name", table_name="products")
    op.drop_table("products")
