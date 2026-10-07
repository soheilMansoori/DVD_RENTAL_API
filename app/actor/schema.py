from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseActorSchema(BaseModel):
    first_name: str = Field(
        ...,
        min_length=4,
        max_length=45,
        description="actor first_name",
        examples=["soheil"],
    )

    last_name: str = Field(
        ...,
        min_length=4,
        max_length=45,
        description="actor last_name",
        examples=["mansoori"],
    )


class CreateActorSchema(BaseActorSchema):
    pass


class UpdateActorSchema(BaseActorSchema):
    pass


class PatchActorSchema(BaseModel):
    first_name: str | None = Field(
        None,
        min_length=4,
        max_length=45,
        description="actor first_name",
        examples=["soheil"],
    )

    last_name: str | None = Field(
        None,
        min_length=4,
        max_length=45,
        description="actor last_name",
        examples=["mansoori"],
    )


class ActorResponseSchema(BaseActorSchema):
    id: int = Field(..., gt=0, description="actor id")
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
