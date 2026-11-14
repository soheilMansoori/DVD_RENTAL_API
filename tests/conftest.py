import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.actor.model import Actor
from app.address.model import Address
from app.city.model import City
from app.core.database import Base
from app.core.dependencies import get_db
from app.country.model import Country
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


# ---------- useful fixtures ----------
@pytest.fixture
def actor(db_session):
    """create one actor and return it"""

    actor = Actor(first_name="soheil", last_name="mansoori")
    db_session.add(actor)
    db_session.commit()
    db_session.refresh(actor)

    yield actor

    existing = db_session.get(Actor, actor.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def country(db_session):
    """create one country and return it"""
    country = Country(country="iran")
    db_session.add(country)
    db_session.commit()
    db_session.refresh(country)

    yield country

    existing = db_session.get(Country, country.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def city(db_session, country):
    """create one city and return it"""
    city = City(city="karaj", country_id=country.id)
    db_session.add(city)
    db_session.commit()
    db_session.refresh(city)

    yield city

    existing = db_session.get(City, city.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def address(db_session, city):
    """create one address and return it"""
    address = Address(
        address="gohardasht street 9",
        district="karaj center",
        phone="09121234567",
        city_id=city.id,
        address2="building number 12 floor 3",
        postal_code="31456",
    )
    db_session.add(address)
    db_session.commit()
    db_session.refresh(address)

    yield address

    existing = db_session.get(City, address.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()
