from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from app.core.dependencies import Pagination, get_db

from .model import Film
from .schema import CreateFilmSchema, PatchFilmSchema, UpdateFilmSchema


class FilmService:
    db: Session
    model: type[Film] = Film

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_all(self, pagination: Pagination):
        page, size, q = (pagination.page, pagination.size, pagination.q)
        model = self.model
        query = self.db.query(model)

        if not q is None:
            query = query.filter(
                or_(
                    model.title.ilike(f"%{q}%"),
                    model.description.ilike(f"%{q}%"),
                )
            )

        total = query.count()
        offset = (page - 1) * size
        items = query.offset(offset).limit(size).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    def get_by_id(self, film_id: int):
        return self.db.query(self.model).filter_by(id=film_id).one_or_none()

    def create(self, data: CreateFilmSchema):
        db, model = (self.db, self.model)

        new_film = model(**data.model_dump())
        db.add(new_film)
        db.commit()
        db.refresh(new_film)

        return new_film

    def update(self, film_id: int, data: UpdateFilmSchema):
        db, model = (self.db, self.model)
        film = db.query(model).filter_by(id=film_id).one_or_none()
        if not film:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(film, key, value)

        db.commit()
        db.refresh(film)
        return film

    def patch(self, film_id: int, data: PatchFilmSchema):
        db, model = (self.db, self.model)
        film = db.query(model).filter_by(id=film_id).one_or_none()
        if not film:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(film, key, value)

        db.commit()
        db.refresh(film)
        return film

    def delete(self, film_id: int):
        db, model = (self.db, self.model)
        film = db.query(model).filter_by(id=film_id).one_or_none()
        if film:
            db.delete(film)
            db.commit()
            return True

        return False
