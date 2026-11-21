from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class BasePaymentSchema(BaseModel):
    customer_id: int = Field(..., gt=0)
    staff_id: int = Field(..., gt=0)
    rental_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0, max_digits=5, decimal_places=2)


class CreatePaymentSchema(BasePaymentSchema):
    pass


class UpdatePaymentSchema(BasePaymentSchema):
    pass


class PatchPaymentSchema(BaseModel):
    customer_id: int | None = Field(None, gt=0)
    staff_id: int | None = Field(None, gt=0)
    rental_id: int | None = Field(None, gt=0)
    amount: Decimal | None = Field(None, gt=0, max_digits=5, decimal_places=2)


class PaymentFiltersSchema(BaseModel):
    customer_id: int | None = Field(None, gt=0)
    staff_id: int | None = Field(None, gt=0)
    rental_id: int | None = Field(None, gt=0)


class PaymentResponseSchema(BasePaymentSchema):
    id: int
    payment_date: datetime
    created_at: datetime
    updated_at: datetime
