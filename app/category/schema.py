from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBaseSchema(BaseModel):
    name: str = Field(
        ...,
        max_length=25,
        description="category name",
        examples=["action"],
    )


class CreateCategorySchema(CategoryBaseSchema):
    pass


class CategoryFiltersSchema(BaseModel):
    name: str | None = Field(
        None,
        max_length=25,
        description="category name",
        examples=["action"],
    )


class CategoryResponseSchema(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
