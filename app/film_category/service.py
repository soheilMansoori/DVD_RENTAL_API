from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import FilmCategory


class FilmCategoryService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = FilmCategory

    def get_categories_by_film(
        self, film_id: int, pagination: Pagination
    ) -> PaginatedResponseSchema[FilmCategory]:
        query = self.db.query(self.model).filter(self.model.film_id == film_id)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = (
            query.order_by(self.model.category_id)
            .limit(pagination.size)
            .offset(offset)
            .all()
        )

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def add_category_to_film(self, film_id: int, category_id: int) -> FilmCategory:
        film_category = self.model(film_id=film_id, category_id=category_id)
        self.db.add(film_category)
        self.db.commit()
        self.db.refresh(film_category)
        return film_category

    def delete_category_from_film(
        self, film_id: int, category_id: int
    ) -> FilmCategory | None:
        film_category = (
            self.db.query(self.model)
            .filter(
                self.model.film_id == film_id,
                self.model.category_id == category_id,
            )
            .one_or_none()
        )

        if not film_category:
            return None

        self.db.delete(film_category)
        self.db.commit()
        return film_category

    def is_category_in_film(self, film_id: int, category_id: int) -> bool:
        exists = (
            self.db.query(self.model)
            .filter(
                self.model.film_id == film_id,
                self.model.category_id == category_id,
            )
            .one_or_none()
        )
        return exists is not None
