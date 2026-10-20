from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseStoreSchema(BaseModel):
    manager_staff_id: int = Field(..., gt=0)
    address_id: int = Field(..., gt=0)


class CreateStoreSchema(BaseStoreSchema):
    pass


class UpdateStoreSchema(BaseStoreSchema):
    pass


class PatchStoreSchema(BaseModel):
    manager_staff_id: int | None = Field(None, gt=0)
    address_id: int | None = Field(None, gt=0)


class StoreResponseSchema(BaseStoreSchema):
    id: int = Field(..., gt=0)
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class PaginatedResponseSchema(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    total_pages: int
