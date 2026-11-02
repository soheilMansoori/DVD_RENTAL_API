from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from app.actor.model import Actor
from app.address.model import Address
from app.category.model import Category
from app.city.model import City
from app.core.database import SessionLocal
from app.country.model import Country
from app.customer.model import Customer
from app.film.model import Film
from app.film_actor.model import FilmActor
from app.film_category.model import FilmCategory
from app.inventory.model import Inventory
from app.language.model import Language
from app.rental.model import Rental
from app.staff.model import Staff
from app.store.model import Store

from .actor import seed_actors
from .address import seed_addresses
from .category import seed_categories
from .city import seed_cities
from .country import seed_countries
from .customer import seed_customers
from .film import seed_films
from .inventory import seed_inventories
from .language import seed_languages
from .rental import seed_rentals
from .staff import seed_staffs
from .store import seed_stores


def clear_database(session):
    try:
        models = [
            Rental,
            Inventory,
            FilmActor,
            FilmCategory,
            Customer,
            Film,
            Store,
            Staff,
            Address,
            City,
            Country,
            Category,
            Language,
            Actor,
        ]

        for model in models:
            session.query(model).delete()

        session.commit()
        print("database clear successfully")

    except SQLAlchemyError as error:
        session.rollback()
        print("error clearing database: ->", error)

    finally:
        session.close()


def main():
    session = SessionLocal()
    faker = Faker()
    try:
        session.execute(text("SET session_replication_role = 'replica';"))
        session.commit()

        clear_database(session=session)

        seed_countries(db=session, faker=faker)
        seed_languages(db=session, faker=faker)
        seed_categories(db=session, faker=faker)
        seed_actors(db=session, faker=faker)
        seed_cities(db=session, faker=faker)
        seed_addresses(db=session, faker=faker)
        seed_films(db=session, faker=faker)
        seed_customers(db=session, faker=faker)
        seed_stores(db=session, faker=faker)
        seed_staffs(db=session, faker=faker)
        seed_inventories(db=session, faker=faker)
        seed_rentals(db=session, faker=faker)

        print("database seed successfully")

    except SQLAlchemyError as error:
        print("seed error ->", error)

    except Exception as error:
        print("unknown error ->", error)

    finally:
        session.close()


if __name__ == "__main__":
    main()
