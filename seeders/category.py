from sqlalchemy.exc import SQLAlchemyError

from app.category.model import Category


def seed_categories(db, faker):
    try:
        data = [
            Category(
                name=faker.name()[:25],
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed categories successfully")

    except SQLAlchemyError as error:
        print("seed categories error ->", error)
