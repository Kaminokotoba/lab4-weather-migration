from datetime import date, datetime
from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session, joinedload
from app.domain.models import Weather


class WeatherRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_country_and_date(self, country: str, target_date: date, location_name: str | None = None):
        start = datetime.combine(target_date, datetime.min.time())
        end = datetime.combine(target_date, datetime.max.time())

        stmt = (
            select(Weather)
            .options(joinedload(Weather.precipitation))
            .where(
                and_(
                    func.lower(Weather.country) == country.lower(),
                    Weather.last_updated >= start,
                    Weather.last_updated <= end,
                )
            )
        )
        if location_name:
            stmt = stmt.where(func.lower(Weather.location_name) == location_name.lower())

        return list(self.session.scalars(stmt).unique().all())
