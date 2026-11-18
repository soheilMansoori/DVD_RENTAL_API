import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.actor.model import Actor
from app.address.model import Address
from app.category.model import Category
from app.city.model import City
from app.core.database import Base
from app.core.dependencies import get_db
from app.country.model import Country
from app.customer.model import Customer
from app.film.model import Film
from app.film_actor.model import FilmActor
from app.language.model import Language
from app.main import app
from app.staff.model import Staff
from app.store.model import Store

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


@pytest.fixture
def category(db_session):
    """create one category and return it"""
    category = Category(name="action")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)

    yield category

    existing = db_session.get(City, category.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def store_and_staff(db_session, address):
    store = Store(manager_staff_id=None, address_id=address.id)
    db_session.add(store)
    db_session.commit()
    db_session.refresh(store)

    staff = Staff(
        first_name="soheil",
        last_name="mansoori",
        address_id=address.id,
        email="soheil@gmail.com",
        store_id=store.id,
        active=True,
        username="soheil_dev",
        password="hashed_password",
    )
    db_session.add(staff)
    db_session.commit()
    db_session.refresh(staff)

    store.manager_staff_id = staff.id
    db_session.commit()
    db_session.refresh(store)

    yield {"store": store, "staff": staff}

    db_session.delete(staff)
    db_session.delete(store)
    db_session.commit()


@pytest.fixture
def store(store_and_staff):
    """create one store and return it"""
    return store_and_staff["store"]


@pytest.fixture
def staff(store_and_staff):
    """create one staff and return it"""
    return store_and_staff["staff"]


@pytest.fixture
def customer(db_session, store, address):
    """create one customer and return it"""
    customer = Customer(
        first_name="soheil",
        last_name="mansoori",
        email="soheil@gmail.com",
        store_id=store.id,
        address_id=address.id,
        active=True,
    )
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    yield customer

    existing = db_session.get(Customer, customer.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def language(db_session):
    """create one language and return it"""
    language = Language(name="english")
    db_session.add(language)
    db_session.commit()
    db_session.refresh(language)

    yield language

    existing = db_session.get(Language, language.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def film(db_session, language):
    """create one film and return it"""
    film = Film(
        title="breaking bad",
        description="HBO film",
        release_year=2008,
        language_id=language.id,
        rental_duration=3,
        rental_rate=4.99,
        length=136,
        replacement_cost=19.99,
    )
    db_session.add(film)
    db_session.commit()
    db_session.refresh(film)

    yield film

    existing = db_session.get(Film, film.id)
    if existing:
        db_session.delete(existing)
        db_session.commit()


@pytest.fixture
def film_actor(db_session, film, actor):
    relation = FilmActor(film_id=film.id, actor_id=actor.id)
    db_session.add(relation)
    db_session.commit()
    db_session.refresh(relation)

    yield relation

    existing = db_session.get(FilmActor, (relation.actor_id, relation.film_id))
    if existing:
        db_session.delete(existing)
        db_session.commit()
