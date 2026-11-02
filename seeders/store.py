from sqlalchemy.exc import SQLAlchemyError

from app.store.model import Store


def seed_stores(db, faker):
    try:
        data = [
            Store(
                manager_staff_id=faker.random_int(1, 100),
                address_id=faker.random_int(1, 100),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed stores successfully")

    except SQLAlchemyError as error:
        print("seed stores error ->", error)
