from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, EmailStr, Field


class BaseStaffSchema(BaseModel):
    first_name: str = Field(..., max_length=45)
    last_name: str = Field(..., max_length=45)
    username: str = Field(..., max_length=16)
    email: EmailStr | None = None
    password: str | None = None
    active: bool = True

    address_id: int = Field(..., gt=0)
    store_id: int = Field(..., gt=0)


class CreateStaffSchema(BaseStaffSchema):
    pass


class UpdatedStaffSchema(BaseStaffSchema):
    pass


class PatchStaffSchema(BaseModel):
    first_name: str | None = Field(None, max_length=45)
    last_name: str | None = Field(None, max_length=45)
    username: str | None = Field(None, max_length=16)
    email: EmailStr | None = None
    password: str | None = None
    active: bool | None = None
    address_id: int | None = Field(None, gt=0)
    store_id: int | None = Field(None, gt=0)


class StaffResponseSchema(BaseStaffSchema):
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
