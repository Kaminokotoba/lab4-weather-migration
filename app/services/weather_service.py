from app.domain.models import Weather


def calculate_is_worth_going_outside(precip_mm=None, humidity=None, wind_kph=None, temperature_celsius=None) -> bool:
    """Проста формула."""
    if precip_mm is not None and precip_mm >= 2.0:
        return False
    if humidity is not None and humidity >= 90 and (precip_mm or 0) > 0:
        return False
    if wind_kph is not None and wind_kph >= 40:
        return False
    return True


def is_worth_going_outside(weather: Weather) -> bool:
    p = weather.precipitation
    return calculate_is_worth_going_outside(
        precip_mm=p.precip_mm if p else None,
        humidity=weather.humidity,
        wind_kph=weather.wind_kph,
        temperature_celsius=weather.temperature_celsius,
    )


class WeatherService:
    def __init__(self, repository):
        self.repo = repository

    def find_weather(self, country, target_date, location_name=None):
        return self.repo.get_by_country_and_date(country, target_date, location_name)