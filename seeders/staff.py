from sqlalchemy.exc import SQLAlchemyError

from app.staff.model import Staff


def seed_staffs(db, faker):
    try:
        data = [
            Staff(
                first_name=faker.first_name()[:45],
                last_name=faker.last_name()[:45],
                email=faker.email()[:50],
                address_id=faker.random_int(1, 100),
                store_id=faker.random_int(1, 100),
                active=faker.boolean(),
                username=faker.user_name()[:16],
                password=faker.password()[:40],
                created_at=faker.date_time(),
                updated_at=faker.date_time(),
            )
            for _ in range(100)
        ]

        db.add_all(data)
        db.commit()
        print("seed staffs successfully")

    except SQLAlchemyError as error:
        print("seed staffs error ->", error)
