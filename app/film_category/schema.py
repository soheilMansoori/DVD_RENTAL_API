from datetime import datetime

from pydantic import BaseModel


class BaseFilmCategorySchema(BaseModel):
    film_id: int
    category_id: int


class FilmCategoryResponseSchema(BaseFilmCategorySchema):
    created_at: datetime
    updated_at: datetime
