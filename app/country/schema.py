from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseCountrySchema(BaseModel):
    country: str = Field(
        ...,
        max_length=50,
        description="country name",
        examples=["iran"],
    )


class CreateCountrySchema(BaseCountrySchema):
    pass


class CountryResponseSchema(BaseCountrySchema):
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
