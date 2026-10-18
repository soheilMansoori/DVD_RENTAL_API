from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseFilmSchema(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="film title",
    )
    description: str | None = Field(
        None,
        max_length=256,
        description="film description",
    )
    release_year: int | None = Field(
        None,
        ge=1950,
        le=datetime.now().year,
        description="film release year",
    )
    language_id: int = Field(..., gt=0)
    rental_duration: int = Field(..., gt=0, description="rental duration in days")
    rental_rate: float = Field(..., ge=0.0, description="rental rate price")
    length: int | None = Field(None, gt=0, description="film length in minutes")
    replacement_cost: float = Field(..., ge=0.0, description="replacement cost price")


class CreateFilmSchema(BaseFilmSchema):
    pass


class UpdateFilmSchema(BaseFilmSchema):
    pass


class PatchFilmSchema(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=128)
    description: str | None = Field(None, max_length=256)
    release_year: int | None = Field(None, ge=1950, le=datetime.now().year)
    language_id: int | None = Field(None, gt=0)
    rental_duration: int | None = Field(None, gt=0)
    rental_rate: float | None = Field(None, ge=0.0)
    length: int | None = Field(None, gt=0)
    replacement_cost: float | None = Field(None, ge=0.0)


class FilmResponseSchema(BaseFilmSchema):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
