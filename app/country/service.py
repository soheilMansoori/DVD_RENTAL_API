from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Country
from .schema import CountryFiltersSchema, CreateCountrySchema


class CountryService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Country

    def get_all(
        self, pagination: Pagination, filters: CountryFiltersSchema
    ) -> PaginatedResponseSchema[Country]:
        query = self.db.query(self.model)

        if filters.country:
            query = query.filter(self.model.country.ilike(f"%{filters.country}%"))

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.limit(pagination.size).offset(offset).all()

        return PaginatedResponseSchema(
            items=items,
            page=pagination.page,
            size=pagination.size,
            total=total,
        )

    def get_by_id(self, country_id: int) -> Country | None:
        return self.db.query(self.model).filter_by(id=country_id).one_or_none()

    def create(self, data: CreateCountrySchema) -> Country:
        new_country = self.model(**data.model_dump())
        self.db.add(new_country)
        self.db.commit()
        self.db.refresh(new_country)
        return new_country

    def delete(self, country_id: int) -> Country | None:
        country = self.db.query(self.model).filter_by(id=country_id).one_or_none()
        if not country:
            return None

        self.db.delete(country)
        self.db.commit()
        return country
