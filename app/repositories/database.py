"""
Data Access layer — database session and engine.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import DATABASE_URL, ECHO_SQL
from app.domain.models import Base


engine = create_engine(DATABASE_URL, echo=ECHO_SQL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_session() -> Session:
    return SessionLocal()


def init_db() -> None:
    """Create all tables (useful for quick tests; prefer Alembic in production)."""
    Base.metadata.create_all(bind=engine)