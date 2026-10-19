from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel


class BaseFilmActorSchema(BaseModel):
    actor_id: int
    film_id: int


class FilmActorResponseSchema(BaseFilmActorSchema):
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
