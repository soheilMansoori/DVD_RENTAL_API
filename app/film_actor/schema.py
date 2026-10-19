from datetime import datetime

from pydantic import BaseModel


class BaseFilmActorSchema(BaseModel):
    actor_id: int
    film_id: int


class FilmActorResponseSchema(BaseFilmActorSchema):
    created_at: datetime
    updated_at: datetime
