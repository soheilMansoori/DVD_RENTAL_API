from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import get_settings

settings = get_settings()

SQL_ALCHEMY_DATABASE_URL = settings.DB_URL

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)

# session
SessionLocal = sessionmaker(engine, autoflush=False, autocommit=False)


# database models base
class Base(DeclarativeBase):
    pass
