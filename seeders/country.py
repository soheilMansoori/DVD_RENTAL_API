from sqlalchemy.exc import SQLAlchemyError

from app.country.model import Country


def seed_countries(db, faker):
    try:
        data = [
            Country(
                country=faker.country()[:50],
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed countries successfully")

    except SQLAlchemyError as error:
        print("seed countries error ->", error)
