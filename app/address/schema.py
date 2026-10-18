from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field


class BaseAddressSchema(BaseModel):
    address: str = Field(
        ...,
        min_length=10,
        max_length=50,
        description="first address",
        examples=["gohardasht street 9"],
    )

    district: str = Field(..., min_length=10, max_length=20, description="district")
    phone: str = Field(..., max_length=20, description="phone number")
    city_id: int = Field(..., gt=0, description="city_id")

    address2: str | None = Field(
        None, min_length=10, max_length=50, description="second address optional"
    )
    postal_code: str | None = Field(
        None, max_length=10, description="postal_code optional"
    )


class CreateAddressSchema(BaseAddressSchema):
    pass


class UpdateAddressSchema(BaseAddressSchema):
    pass


class PatchAddressSchema(BaseModel):
    address: str | None = Field(
        None,
        min_length=10,
        max_length=50,
        description="first address",
        examples=["gohardasht street 9"],
    )

    district: str | None = Field(
        None, min_length=10, max_length=20, description="district"
    )
    phone: str | None = Field(None, max_length=20, description="phone number")
    city_id: int | None = Field(None, gt=0, description="city_id")
    address2: str | None = Field(
        None, min_length=10, max_length=50, description="second address optional"
    )
    postal_code: str | None = Field(
        None, max_length=10, description="postal_code optional"
    )


class AddressResponseSchema(BaseAddressSchema):
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
