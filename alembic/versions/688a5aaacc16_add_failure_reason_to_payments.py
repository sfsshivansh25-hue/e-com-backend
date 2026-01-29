

"""add failure_reason to payments

Revision ID: 688a5aaacc16
Revises: <PREVIOUS_REVISION_ID>
Create Date: 2026-01-29
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "688a5aaacc16"
down_revision = "6a7ed2051760"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "payments",
        sa.Column("failure_reason", sa.String(length=255), nullable=True),
    )


def downgrade():
    op.drop_column("payments", "failure_reason")
