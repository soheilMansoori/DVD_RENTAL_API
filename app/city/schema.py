from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseCitySchema(BaseModel):
    city: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="city name",
        examples=["karaj"],
    )

    country_id: int = Field(
        ...,
        gt=0,
        description="country id",
    )


class CreateCitySchema(BaseCitySchema):
    pass


class CityResponseSchema(BaseCitySchema):
    id: int
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
