from sqlalchemy.exc import SQLAlchemyError

from app.language.model import Language


def seed_languages(db, faker):
    try:
        data = [
            Language(
                name=faker.name()[:20],
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed languages successfully")

    except SQLAlchemyError as error:
        print("seed languages error ->", error)
