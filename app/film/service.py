from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Film
from .schema import (
    CreateFilmSchema,
    FileFiltersSchema,
    PatchFilmSchema,
    UpdateFilmSchema,
)


class FilmService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Film

    def get_all(
        self, pagination: Pagination, filters: FileFiltersSchema
    ) -> PaginatedResponseSchema[Film]:
        query = self.db.query(self.model)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.offset(offset).limit(pagination.size).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, film_id: int) -> Film | None:
        return self.db.query(self.model).filter_by(id=film_id).one_or_none()

    def create(self, data: CreateFilmSchema) -> Film:
        new_film = self.model(**data.model_dump())
        self.db.add(new_film)
        self.db.commit()
        self.db.refresh(new_film)
        return new_film

    def update(self, film_id: int, data: UpdateFilmSchema) -> Film | None:
        film = self.db.query(self.model).filter_by(id=film_id).one_or_none()
        if not film:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(film, key, value)

        self.db.commit()
        self.db.refresh(film)
        return film

    def patch(self, film_id: int, data: PatchFilmSchema) -> Film | None:
        film = self.db.query(self.model).filter_by(id=film_id).one_or_none()
        if not film:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(film, key, value)

        self.db.commit()
        self.db.refresh(film)
        return film

    def delete(self, film_id: int) -> Film | None:
        film = self.db.query(self.model).filter_by(id=film_id).one_or_none()
        if not film:
            return None

        self.db.delete(film)
        self.db.commit()
        return film
