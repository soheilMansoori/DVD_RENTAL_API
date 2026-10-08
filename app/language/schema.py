from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseLanguageSchema(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=20,
        description="language name",
        examples=["english"],
    )


class CreateLanguageSchema(BaseLanguageSchema):
    pass


class LanguageResponseSchema(BaseLanguageSchema):
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
