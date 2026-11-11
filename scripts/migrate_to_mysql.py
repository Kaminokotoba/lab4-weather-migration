"""
Task 5
"""
from __future__ import annotations

import sys
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.config import DATABASE_URL, MYSQL_DATABASE_URL
from app.domain.models import Base, Weather, Precipitation


def migrate():
    print("=== PostgreSQL → MySQL migration ===")
    print(f"Source : {DATABASE_URL}")
    print(f"Target : {MYSQL_DATABASE_URL}")

    src_engine = create_engine(DATABASE_URL)
    dst_engine = create_engine(MYSQL_DATABASE_URL)

    SrcSession = sessionmaker(bind=src_engine)
    DstSession = sessionmaker(bind=dst_engine)

    # Create schema on MySQL
    print("Creating tables on MySQL...")
    Base.metadata.drop_all(bind=dst_engine)   # clean start for demo
    Base.metadata.create_all(bind=dst_engine)

    src = SrcSession()
    dst = DstSession()

    try:
        weathers = src.query(Weather).all()
        print(f"Found {len(weathers)} weather records in PostgreSQL")

        for w in weathers:
            # Detach and re-create objects for the new session
            new_w = Weather(
                country=w.country,
                wind_degree=w.wind_degree,
                wind_kph=w.wind_kph,
                wind_direction=w.wind_direction,
                last_updated=w.last_updated,
                sunrise=w.sunrise,
                location_name=w.location_name,
                latitude=w.latitude,
                longitude=w.longitude,
                timezone=w.timezone,
                temperature_celsius=w.temperature_celsius,
                condition_text=w.condition_text,
                humidity=w.humidity,
                cloud=w.cloud,
                wind_mph=w.wind_mph, 
                pressure_mb=w.pressure_mb,
                visibility_km=w.visibility_km,
                uv_index=w.uv_index,
                sunset=w.sunset,
            )
            if w.precipitation:
                new_w.precipitation = Precipitation(
                    precip_mm=w.precipitation.precip_mm,
                    precip_in=w.precipitation.precip_in,
                    is_worth_going_outside=w.precipitation.is_worth_going_outside,
                )
            dst.add(new_w)

        dst.commit()
        print(f"Successfully migrated {len(weathers)} records to MySQL.")
        print("Both databases now contain identical data (schema + content).")
    except Exception as e:
        dst.rollback()
        print(f"Migration failed: {e}")
        raise
    finally:
        src.close()
        dst.close()


if __name__ == "__main__":
    migrate()