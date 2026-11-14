from datetime import datetime

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


class CategoryFiltersSchema(BaseModel):
    name: str | None = Field(
        None,
        max_length=25,
        description="category name",
        examples=["action"],
    )


class CategoryResponseSchema(BaseCategorySchema):
    id: int
    created_at: datetime
    updated_at: datetime
