from sqlalchemy.exc import SQLAlchemyError

from app.city.model import City


def seed_cities(db, faker):
    try:
        data = [
            City(
                city=faker.name()[:50],
                country_id=faker.random_int(1, 100),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed cities successfully")

    except SQLAlchemyError as error:
        print("seed cities error ->", error)
