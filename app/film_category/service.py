from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db

from .model import FilmCategory


class FilmCategoryService:
    db: Session
    model: type[FilmCategory] = FilmCategory

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_categories_by_film(self, film_id: int, pagination: Pagination):
        page, size = pagination.page, pagination.size
        db, model = self.db, self.model

        query = db.query(model).filter(model.film_id == film_id)

        total = query.count()
        offset = (page - 1) * size
        items = query.order_by(model.category_id).limit(size).offset(offset).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    def add_category_to_film(self, film_id: int, category_id: int):
        db, model = self.db, self.model
        film_category = model(film_id=film_id, category_id=category_id)
        db.add(film_category)
        db.commit()
        db.refresh(film_category)
        return film_category

    def delete_category_from_film(self, film_id: int, category_id: int):
        db, model = self.db, self.model
        film_category = (
            db.query(model)
            .filter(
                model.film_id == film_id,
                model.category_id == category_id,
            )
            .one_or_none()
        )

        if film_category is None:
            return False

        db.delete(film_category)
        db.commit()
        return True

    def is_category_in_film(self, film_id: int, category_id: int):
        db, model = self.db, self.model
        exists = (
            db.query(model)
            .filter(
                model.film_id == film_id,
                model.category_id == category_id,
            )
            .one_or_none()
        )
        return exists is not None
