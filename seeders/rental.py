from sqlalchemy.exc import SQLAlchemyError

from app.rental.model import Rental


def seed_rentals(db, faker):
    try:
        data = [
            Rental(
                inventory_id=faker.random_int(1, 100),
                customer_id=faker.random_int(1, 100),
                staff_id=faker.random_int(1, 100),
                return_date=faker.date(),
                rental_date=faker.date(),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed rentals successfully")

    except SQLAlchemyError as error:
        print("seed rentals error ->", error)
