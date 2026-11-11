import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.repositories.database import get_session
from app.repositories.weather_repository import WeatherRepository


def main():
    print("Пошук погоди")
    country = input("Країна: ").strip()
    date_str = input("Дата (YYYY-MM-DD): ").strip()
    location = input("Місто (можна пропустити): ").strip() or None

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        print("Невірний формат дати")
        return

    session = get_session()
    try:
        repo = WeatherRepository(session)
        results = repo.get_by_country_and_date(country, target_date, location)

        if not results:
            print("Нічого не знайдено")
            return

        for w in results:
            print("-" * 40)
            print(f"{w.country}, {w.location_name}")
            print(f"Оновлено: {w.last_updated}")
            print(f"Температура: {w.temperature_celsius}°C")
            print(f"Вітер: {w.wind_kph} км/год, {w.wind_direction}")
            print(f"Схід: {w.sunrise}")
            if w.precipitation:
                print(f"Опади: {w.precipitation.precip_mm} мм")
                worth = w.precipitation.is_worth_going_outside
                print(f"Виходити: {'так' if worth else 'ні'}")
            print("-" * 40)
    finally:
        session.close()


if __name__ == "__main__":
    main()
