"""Initial schema — single weather table (before refactor)

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "weather",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("country", sa.String(length=100), nullable=False),
        sa.Column("wind_degree", sa.Integer(), nullable=True),
        sa.Column("wind_kph", sa.Float(), nullable=True),
        sa.Column("wind_direction", sa.Enum(
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW",
            name="wind_direction_enum", native_enum=False
        ), nullable=True),
        sa.Column("last_updated", sa.DateTime(), nullable=True),
        sa.Column("sunrise", sa.Time(), nullable=True),
        sa.Column("location_name", sa.String(length=150), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("timezone", sa.String(length=50), nullable=True),
        sa.Column("temperature_celsius", sa.Float(), nullable=True),
        sa.Column("condition_text", sa.String(length=100), nullable=True),
        sa.Column("humidity", sa.Integer(), nullable=True),
        sa.Column("cloud", sa.Integer(), nullable=True),
        sa.Column("wind_mph", sa.Float(), nullable=True),
        sa.Column("gust_kph", sa.Float(), nullable=True),
        sa.Column("pressure_mb", sa.Float(), nullable=True),
        sa.Column("visibility_km", sa.Float(), nullable=True),
        sa.Column("uv_index", sa.Float(), nullable=True),
        sa.Column("sunset", sa.Time(), nullable=True),
        # Temporary columns for precipitation (will be moved in next migration)
        sa.Column("precip_mm", sa.Float(), nullable=True),
        sa.Column("precip_in", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("country", "location_name", "last_updated", name="uq_weather_location_time"),
    )
    op.create_index("ix_weather_country", "weather", ["country"])
    op.create_index("ix_weather_last_updated", "weather", ["last_updated"])


def downgrade() -> None:
    op.drop_index("ix_weather_last_updated", table_name="weather")
    op.drop_index("ix_weather_country", table_name="weather")
    op.drop_table("weather")
