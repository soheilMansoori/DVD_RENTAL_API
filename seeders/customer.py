from sqlalchemy.exc import SQLAlchemyError

from app.customer.model import Customer


def seed_customers(db, faker):
    try:
        data = [
            Customer(
                first_name=faker.first_name()[:45],
                last_name=faker.last_name()[:45],
                email=faker.email()[:50],
                active=faker.boolean(),
                store_id=faker.random_int(1, 100),
                address_id=faker.random_int(1, 100),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed customers successfully")

    except SQLAlchemyError as error:
        print("seed customers error ->", error)
