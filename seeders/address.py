from sqlalchemy.exc import SQLAlchemyError

from app.address.model import Address


def seed_addresses(db, faker):
    try:
        data = [
            Address(
                address=faker.street_address()[:50],
                address2=faker.secondary_address()[:50],
                district=faker.word()[:20],
                postal_code=faker.postcode()[:10],
                phone=faker.phone_number()[:20],
                city_id=faker.random_int(min=1, max=100),
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()

        print("seed addresses successfully")

    except SQLAlchemyError as error:
        print("seed addresses error ->", error)
