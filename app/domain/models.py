from datetime import datetime, time
from enum import Enum
from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class WindDirection(str, Enum):
    N = "N"
    NNE = "NNE"
    NE = "NE"
    ENE = "ENE"
    E = "E"
    ESE = "ESE"
    SE = "SE"
    SSE = "SSE"
    S = "S"
    SSW = "SSW"
    SW = "SW"
    WSW = "WSW"
    W = "W"
    WNW = "WNW"
    NW = "NW"
    NNW = "NNW"


class Weather(Base):
    __tablename__ = "weather"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100), index=True)
    location_name: Mapped[str | None] = mapped_column(String(150))
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    timezone: Mapped[str | None] = mapped_column(String(50))
    last_updated: Mapped[datetime | None] = mapped_column(DateTime, index=True)
    temperature_celsius: Mapped[float | None] = mapped_column(Float)
    condition_text: Mapped[str | None] = mapped_column(String(100))
    wind_mph: Mapped[float | None] = mapped_column(Float)
    wind_kph: Mapped[float | None] = mapped_column(Float)
    wind_degree: Mapped[int | None] = mapped_column(Integer)
    wind_direction: Mapped[WindDirection | None] = mapped_column(
        SQLEnum(WindDirection, native_enum=False)
    )
    humidity: Mapped[int | None] = mapped_column(Integer)
    cloud: Mapped[int | None] = mapped_column(Integer)
    pressure_mb: Mapped[float | None] = mapped_column(Float)
    visibility_km: Mapped[float | None] = mapped_column(Float)
    uv_index: Mapped[float | None] = mapped_column(Float)
    sunrise: Mapped[time | None] = mapped_column(Time)
    sunset: Mapped[time | None] = mapped_column(Time)

    precipitation: Mapped["Precipitation | None"] = relationship(
        back_populates="weather", uselist=False, cascade="all, delete-orphan"
    )


class Precipitation(Base):
    __tablename__ = "precipitation"

    id: Mapped[int] = mapped_column(primary_key=True)
    weather_id: Mapped[int] = mapped_column(ForeignKey("weather.id", ondelete="CASCADE"), unique=True)
    precip_mm: Mapped[float | None] = mapped_column(Float)
    precip_in: Mapped[float | None] = mapped_column(Float)
    is_worth_going_outside: Mapped[bool | None] = mapped_column(Boolean)

    weather: Mapped["Weather"] = relationship(back_populates="precipitation")
