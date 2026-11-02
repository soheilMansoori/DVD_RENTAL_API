from sqlalchemy.exc import SQLAlchemyError

from app.inventory.model import Inventory


def seed_inventories(db, faker):
    try:
        data = [
            Inventory(
                film_id=faker.random_int(1, 100),
                store_id=faker.random_int(1, 100),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed inventories")

    except SQLAlchemyError as error:
        print("seed inventories error ->", error)
