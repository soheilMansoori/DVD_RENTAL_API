from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, EmailStr, Field


class BaseCustomerSchema(BaseModel):
    first_name: str = Field(..., max_length=45)
    last_name: str = Field(..., max_length=45)
    email: EmailStr | None = None
    active: bool = True

    address_id: int = Field(..., gt=0)
    store_id: int = Field(..., gt=0)


class CreateCustomerSchema(BaseCustomerSchema):
    pass


class UpdatedCustomerSchema(BaseCustomerSchema):
    pass


class PatchCustomerSchema(BaseModel):
    first_name: str | None = Field(None, max_length=45)
    last_name: str | None = Field(None, max_length=45)
    email: EmailStr | None = None
    active: bool | None = None
    address_id: int | None = Field(None, gt=0)
    store_id: int | None = Field(None, gt=0)


class CustomerResponseSchema(BaseCustomerSchema):
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
