from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import FilmActor


class FilmActorService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = FilmActor

    def get_actors_by_film(
        self, film_id: int, pagination: Pagination
    ) -> PaginatedResponseSchema[FilmActor]:
        query = self.db.query(self.model).filter(self.model.film_id == film_id)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = (
            query.order_by(self.model.actor_id)
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

    def add_actor_to_film(self, film_id: int, actor_id: int) -> FilmActor:
        film_actor = self.model(film_id=film_id, actor_id=actor_id)
        self.db.add(film_actor)
        self.db.commit()
        self.db.refresh(film_actor)
        return film_actor

    def delete_actor_from_film(self, film_id: int, actor_id: int) -> FilmActor | None:
        film_actor = (
            self.db.query(self.model)
            .filter(self.model.film_id == film_id, self.model.actor_id == actor_id)
            .one_or_none()
        )

        if not film_actor:
            return None

        self.db.delete(film_actor)
        self.db.commit()
        return film_actor

    def is_actor_in_film(self, film_id: int, actor_id: int) -> bool:
        exists = (
            self.db.query(self.model)
            .filter(self.model.film_id == film_id, self.model.actor_id == actor_id)
            .one_or_none()
        )
        return exists is not None
