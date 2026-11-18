from datetime import datetime

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


class CustomerFiltersSchema(PatchCustomerSchema):
    pass


class CustomerResponseSchema(BaseCustomerSchema):
    id: int
    created_at: datetime
    updated_at: datetime
