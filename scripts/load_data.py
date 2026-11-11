"""Завантаження даних з CSV."""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.domain.models import Weather, Precipitation, WindDirection
from app.repositories.database import get_session, init_db
from app.services.weather_service import calculate_is_worth_going_outside

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "GlobalWeatherRepository.csv"


def parse_time(value):
    if pd.isna(value) or value is None:
        return None
    value = str(value).strip()
    for fmt in ("%I:%M %p", "%H:%M", "%H:%M:%S"):
        try:
            return datetime.strptime(value, fmt).time()
        except ValueError:
            continue
    return None


def parse_datetime(value):
    if pd.isna(value) or value is None:
        return None
    try:
        return pd.to_datetime(value).to_pydatetime()
    except Exception:
        return None


def safe_enum(value):
    if pd.isna(value) or value is None:
        return None
    try:
        return WindDirection(str(value).strip().upper())
    except ValueError:
        return None


def load(limit=None):
    print(f"Читаю CSV: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    if limit:
        df = df.head(limit)
    print(f"Рядків: {len(df)}")

    init_db()
    session = get_session()

    try:
        count = 0
        for _, row in df.iterrows():
            weather = Weather(
                country=str(row.get("country", ""))[:100],
                location_name=str(row.get("location_name", ""))[:150] if pd.notna(row.get("location_name")) else None,
                latitude=float(row["latitude"]) if pd.notna(row.get("latitude")) else None,
                longitude=float(row["longitude"]) if pd.notna(row.get("longitude")) else None,
                timezone=str(row.get("timezone", ""))[:50] if pd.notna(row.get("timezone")) else None,
                last_updated=parse_datetime(row.get("last_updated")),
                temperature_celsius=float(row["temperature_celsius"]) if pd.notna(row.get("temperature_celsius")) else None,
                condition_text=str(row.get("condition_text", ""))[:100] if pd.notna(row.get("condition_text")) else None,
                wind_mph=float(row["wind_mph"]) if pd.notna(row.get("wind_mph")) else None,
                wind_kph=float(row["wind_kph"]) if pd.notna(row.get("wind_kph")) else None,
                wind_degree=int(row["wind_degree"]) if pd.notna(row.get("wind_degree")) else None,
                wind_direction=safe_enum(row.get("wind_direction")),
                humidity=int(row["humidity"]) if pd.notna(row.get("humidity")) else None,
                cloud=int(row["cloud"]) if pd.notna(row.get("cloud")) else None,
                pressure_mb=float(row["pressure_mb"]) if pd.notna(row.get("pressure_mb")) else None,
                visibility_km=float(row["visibility_km"]) if pd.notna(row.get("visibility_km")) else None,
                uv_index=float(row["uv_index"]) if pd.notna(row.get("uv_index")) else None,
                sunrise=parse_time(row.get("sunrise")),
                sunset=parse_time(row.get("sunset")),
            )

            precip_mm = float(row["precip_mm"]) if pd.notna(row.get("precip_mm")) else None
            precip_in = float(row["precip_in"]) if pd.notna(row.get("precip_in")) else None

            worth = calculate_is_worth_going_outside(
                precip_mm=precip_mm,
                humidity=weather.humidity,
                wind_kph=weather.wind_kph,
            )

            weather.precipitation = Precipitation(
                precip_mm=precip_mm,
                precip_in=precip_in,
                is_worth_going_outside=worth,
            )

            session.add(weather)
            count += 1
            if count % 500 == 0:
                session.commit()
                print(f"  збережено {count} рядків...")

        session.commit()
        print(f"Завантажено {count} записів.")
    except Exception as e:
        session.rollback()
        print(f"Помилка: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    load(limit=args.limit)
