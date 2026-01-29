"""create users table


Revision ID: xxxx_create_users
Revises: c7090cbe08a0
Create Date: 2026-01-28
"""


from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "ec1746123bd5"
down_revision = "c7090cbe08a0"
branch_labels = None
depends_on = None




def upgrade():
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

def downgrade():
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")