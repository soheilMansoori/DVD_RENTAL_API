from sqlalchemy.exc import SQLAlchemyError

from app.film.model import Film


def seed_films(db, faker):
    try:
        data = [
            Film(
                title=faker.name()[:128],
                description=faker.text(),
                release_year=faker.year(),
                length=faker.random_int(60, 360),
                language_id=faker.random_int(1, 100),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed films successfully")

    except SQLAlchemyError as error:
        print("seed films error ->", error)
