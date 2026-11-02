from sqlalchemy.exc import SQLAlchemyError

from app.actor.model import Actor


def seed_actors(db, faker):
    try:
        data = [
            Actor(
                first_name=faker.first_name()[:45],
                last_name=faker.last_name()[:45],
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()

        print("seed actors successfully")

    except SQLAlchemyError as error:
        print("seed actors error ->", error)
