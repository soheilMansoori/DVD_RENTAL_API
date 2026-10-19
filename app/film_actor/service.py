from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db

from .model import FilmActor


class FilmActorService:
    db: Session
    model: type[FilmActor] = FilmActor

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_actors_by_film(self, film_id: int):
        return self.db.query(self.model).filter(self.model.film_id == film_id).all()

    def add_actor_to_film(self, film_id: int, actor_id: int):
        db, model = self.db, self.model
        film_actor = model(film_id=film_id, actor_id=actor_id)
        db.add(film_actor)
        db.commit()
        db.refresh(film_actor)
        return film_actor

    def delete_actor_from_film(self, film_id: int, actor_id: int):
        db, model = self.db, self.model
        film_actor = (
            db.query(model)
            .filter(model.film_id == film_id, model.actor_id == actor_id)
            .one_or_none()
        )

        if film_actor is None:
            return False

        db.delete(film_actor)
        db.commit()
        return True

    def is_actor_in_film(self, film_id: int, actor_id: int):
        exists = (
            self.db.query(self.model)
            .filter(self.model.film_id == film_id, self.model.actor_id == actor_id)
            .one_or_none()
        )
        return exists is not None
