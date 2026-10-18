from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseCategorySchema(BaseModel):
    name: str = Field(
        ...,
        max_length=25,
        description="category name",
        examples=["action"],
    )


class CreateCategorySchema(BaseCategorySchema):
    pass


class CategoryResponseSchema(BaseCategorySchema):
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
