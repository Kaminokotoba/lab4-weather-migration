"""
Optional script: recalculate is_worth_going_outside for all existing rows.
Useful after changing the formula.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.repositories.database import get_session
from app.repositories.weather_repository import WeatherRepository
from app.services.weather_service import WeatherService


def main():
    session = get_session()
    try:
        repo = WeatherRepository(session)
        service = WeatherService(repo)
        weathers = repo.get_all(limit=100000)
        updated = 0
        for w in weathers:
            if w.precipitation:
                service.fill_is_worth_going_outside(w)
                updated += 1
        session.commit()
        print(f"Updated is_worth_going_outside for {updated} records.")
    finally:
        session.close()


if __name__ == "__main__":
    main()