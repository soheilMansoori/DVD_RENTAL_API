from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import City
from .schema import CityFiltersSchema, CreateCitySchema


class CityService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = City

    def get_all(
        self, pagination: Pagination, filters: CityFiltersSchema
    ) -> PaginatedResponseSchema[City]:

        query = self.db.query(self.model)

        if filters.city:
            query = query.filter(self.model.city.ilike(f"%{filters.city}%"))

        if filters.country_id:
            query = query.filter_by(country_id=filters.country_id)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.limit(pagination.size).offset(offset).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, city_id: int) -> City | None:
        return (
            self.db.query(self.model)
            .filter_by(id=city_id)
            .options(joinedload(self.model.country))
            .one_or_none()
        )

    def create(self, data: CreateCitySchema) -> City:
        new_city = self.model(**data.model_dump())
        self.db.add(new_city)
        self.db.commit()
        self.db.refresh(new_city)
        return new_city

    def delete(self, city_id: int) -> City | None:
        city = self.db.query(self.model).filter_by(id=city_id).one_or_none()
        if not city:
            return None

        self.db.delete(city)
        self.db.commit()
        return city
