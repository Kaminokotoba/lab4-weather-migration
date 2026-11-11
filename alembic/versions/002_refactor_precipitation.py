"""Refactor: move precipitation columns to separate table + add boolean column

This migration:
1. Creates precipitation table
2. Copies existing precip_mm / precip_in data (no data loss)
3. Adds is_worth_going_outside boolean column (nullable, no hard default)
4. Drops old columns from weather table
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create new table
    op.create_table(
        "precipitation",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("weather_id", sa.Integer(), nullable=False),
        sa.Column("precip_mm", sa.Float(), nullable=True),
        sa.Column("precip_in", sa.Float(), nullable=True),
        sa.Column(
            "is_worth_going_outside",
            sa.Boolean(),
            nullable=True,
            comment="Whether it is worth going outside based on precipitation and related conditions",
        ),
        sa.ForeignKeyConstraint(["weather_id"], ["weather.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("weather_id"),
    )
    op.create_index("ix_precipitation_weather_id", "precipitation", ["weather_id"])

    # 2. Copy data (preserve existing values — no data loss)
    op.execute(
        """
        INSERT INTO precipitation (weather_id, precip_mm, precip_in, is_worth_going_outside)
        SELECT id, precip_mm, precip_in, NULL
        FROM weather
        WHERE precip_mm IS NOT NULL OR precip_in IS NOT NULL
        """
    )

    # 3. Drop old columns from weather
    op.drop_column("weather", "precip_mm")
    op.drop_column("weather", "precip_in")


def downgrade() -> None:
    # Add columns back
    op.add_column("weather", sa.Column("precip_mm", sa.Float(), nullable=True))
    op.add_column("weather", sa.Column("precip_in", sa.Float(), nullable=True))

    # Copy data back
    op.execute(
        """
        UPDATE weather w
        SET precip_mm = p.precip_mm,
            precip_in = p.precip_in
        FROM precipitation p
        WHERE w.id = p.weather_id
        """
    )

    op.drop_index("ix_precipitation_weather_id", table_name="precipitation")
    op.drop_table("precipitation")
