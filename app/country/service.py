from math import ceil

from sqlalchemy.orm import Session

from .model import Country
from .schema import CreateCountrySchema


class CountryService:
    @staticmethod
    def get_all(
        db: Session,
        page: int = 1,
        size: int = 10,
    ):
        total = db.query(Country).count()
        offset = (page - 1) * size
        items = db.query(Country).limit(size).offset(offset).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    @staticmethod
    def create(db: Session, data: CreateCountrySchema):
        new_country = Country(**data.model_dump())
        db.add(new_country)
        db.commit()
        db.refresh(new_country)
        return new_country

    @staticmethod
    def delete(db: Session, country_id: int):
        country = db.query(Country).filter_by(id=country_id).one_or_none()
        if country:
            db.delete(country)
            db.commit()
            return True
        return False
