from datetime import datetime

from pydantic import BaseModel, Field


class BaseRentalSchema(BaseModel):
    inventory_id: int = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    staff_id: int = Field(..., gt=0)
    return_date: datetime | None = None


class CreateRentalSchema(BaseModel):
    inventory_id: int = Field(..., gt=0)
    customer_id: int = Field(..., gt=0)
    staff_id: int = Field(..., gt=0)


class UpdateRentalSchema(BaseRentalSchema):
    pass


class PatchRentalSchema(BaseModel):
    inventory_id: int | None = Field(None, gt=0)
    customer_id: int | None = Field(None, gt=0)
    staff_id: int | None = Field(None, gt=0)
    return_date: datetime | None = None


class RentalFiltersSchema(BaseModel):
    inventory_id: int | None = Field(None, gt=0)
    customer_id: int | None = Field(None, gt=0)
    staff_id: int | None = Field(None, gt=0)


class RentalResponseSchema(BaseModel):
    id: int
    rental_date: datetime
    inventory_id: int
    customer_id: int
    return_date: datetime | None
    staff_id: int
    created_at: datetime
    updated_at: datetime
