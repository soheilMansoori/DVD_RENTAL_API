from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.core.schemas import PaginatedResponseSchema
from app.customer.service import CustomerService
from app.rental.service import RentalService
from app.staff.service import StaffService

from .schema import (
    CreatePaymentSchema,
    PatchPaymentSchema,
    PaymentFiltersSchema,
    PaymentResponseSchema,
    UpdatePaymentSchema,
)
from .service import PaymentService

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=PaginatedResponseSchema[PaymentResponseSchema])
def get_all_payments(
    payment_service: Annotated[PaymentService, Depends(PaymentService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
    filters: Annotated[PaymentFiltersSchema, Depends(PaymentFiltersSchema)],
):
    return payment_service.get_all(pagination, filters)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=PaymentResponseSchema
)
def create_payment(
    payment_service: Annotated[PaymentService, Depends(PaymentService)],
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    staff_service: Annotated[StaffService, Depends(StaffService)],
    rental_service: Annotated[RentalService, Depends(RentalService)],
    data: CreatePaymentSchema,
):
    # validate customer
    customer = customer_service.get_by_id(data.customer_id)
    if not customer:
        raise NotFoundException("customer not found")

    # validate staff
    staff = staff_service.get_by_id(data.staff_id)
    if not staff:
        raise NotFoundException("staff not found")

    # validate rental
    rental = rental_service.get_by_id(data.rental_id)
    if not rental:
        raise NotFoundException("rental not found")

    return payment_service.create(data)


@router.get("/{payment_id}", response_model=PaymentResponseSchema)
def get_payment_by_id(
    payment_service: Annotated[PaymentService, Depends(PaymentService)],
    payment_id: Annotated[int, Path(gt=0)],
):
    payment = payment_service.get_by_id(payment_id)
    if not payment:
        raise NotFoundException()
    return payment


@router.put("/{payment_id}", response_model=PaymentResponseSchema)
def update_payment_by_id(
    payment_service: Annotated[PaymentService, Depends(PaymentService)],
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    staff_service: Annotated[StaffService, Depends(StaffService)],
    rental_service: Annotated[RentalService, Depends(RentalService)],
    payment_id: Annotated[int, Path(gt=0)],
    data: UpdatePaymentSchema,
):
    payment = payment_service.get_by_id(payment_id)
    if not payment:
        raise NotFoundException()

    customer = customer_service.get_by_id(data.customer_id)
    if not customer:
        raise NotFoundException("customer not found")

    staff = staff_service.get_by_id(data.staff_id)
    if not staff:
        raise NotFoundException("staff not found")

    rental = rental_service.get_by_id(data.rental_id)
    if not rental:
        raise NotFoundException("rental not found")

    return payment_service.update(payment_id, data)


@router.patch("/{payment_id}", response_model=PaymentResponseSchema)
def patch_payment_by_id(
    payment_service: Annotated[PaymentService, Depends(PaymentService)],
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    staff_service: Annotated[StaffService, Depends(StaffService)],
    rental_service: Annotated[RentalService, Depends(RentalService)],
    payment_id: Annotated[int, Path(gt=0)],
    data: PatchPaymentSchema,
):
    payment = payment_service.get_by_id(payment_id)
    if not payment:
        raise NotFoundException()

    if data.customer_id is not None:
        customer = customer_service.get_by_id(data.customer_id)
        if not customer:
            raise NotFoundException("customer not found")

    if data.staff_id is not None:
        staff = staff_service.get_by_id(data.staff_id)
        if not staff:
            raise NotFoundException("staff not found")

    if data.rental_id is not None:
        rental = rental_service.get_by_id(data.rental_id)
        if not rental:
            raise NotFoundException("rental not found")

    return payment_service.patch(payment_id, data)


@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_by_id(
    payment_service: Annotated[PaymentService, Depends(PaymentService)],
    payment_id: Annotated[int, Path(gt=0)],
):
    result = payment_service.delete(payment_id)
    if not result:
        raise NotFoundException()
