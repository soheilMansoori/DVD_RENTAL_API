from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.core.schemas import PaginatedResponseSchema
from app.customer.service import CustomerService
from app.inventory.service import InventoryService
from app.staff.service import StaffService

from .schema import (
    CreateRentalSchema,
    PatchRentalSchema,
    RentalFiltersSchema,
    RentalResponseSchema,
    UpdateRentalSchema,
)
from .service import RentalService

router = APIRouter(prefix="/rentals", tags=["Rentals"])


@router.get("/", response_model=PaginatedResponseSchema[RentalResponseSchema])
def get_all_rentals(
    rental_service: Annotated[RentalService, Depends(RentalService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
    filters: Annotated[RentalFiltersSchema, Depends(RentalFiltersSchema)],
):
    return rental_service.get_all(pagination, filters)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=RentalResponseSchema
)
def create_rental(
    rental_service: Annotated[RentalService, Depends(RentalService)],
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    staff_service: Annotated[StaffService, Depends(StaffService)],
    data: CreateRentalSchema,
):
    # validate inventory
    inventory = inventory_service.get_by_id(data.inventory_id)
    if not inventory:
        raise NotFoundException("inventory not found")

    # validate customer
    customer = customer_service.get_by_id(data.customer_id)
    if not customer:
        raise NotFoundException("customer not found")

    # validate staff
    staff = staff_service.get_by_id(data.staff_id)
    if not staff:
        raise NotFoundException("staff not found")

    return rental_service.create(data)


@router.get("/{rental_id}", response_model=RentalResponseSchema)
def get_rental_by_id(
    rental_service: Annotated[RentalService, Depends(RentalService)],
    rental_id: Annotated[int, Path(gt=0)],
):
    rental = rental_service.get_by_id(rental_id)
    if not rental:
        raise NotFoundException()
    return rental


@router.put("/{rental_id}", response_model=RentalResponseSchema)
def update_rental_by_id(
    rental_service: Annotated[RentalService, Depends(RentalService)],
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    staff_service: Annotated[StaffService, Depends(StaffService)],
    rental_id: Annotated[int, Path(gt=0)],
    data: UpdateRentalSchema,
):
    rental = rental_service.get_by_id(rental_id)
    if not rental:
        raise NotFoundException()

    # validate inventory
    inventory = inventory_service.get_by_id(data.inventory_id)
    if not inventory:
        raise NotFoundException("inventory not found")

    # validate customer
    customer = customer_service.get_by_id(data.customer_id)
    if not customer:
        raise NotFoundException("customer not found")

    # Validate staff
    staff = staff_service.get_by_id(data.staff_id)
    if not staff:
        raise NotFoundException("staff not found")

    return rental_service.update(rental_id, data)


@router.patch("/{rental_id}", response_model=RentalResponseSchema)
def patch_rental_by_id(
    rental_service: Annotated[RentalService, Depends(RentalService)],
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    staff_service: Annotated[StaffService, Depends(StaffService)],
    rental_id: Annotated[int, Path(gt=0)],
    data: PatchRentalSchema,
):
    rental = rental_service.get_by_id(rental_id)
    if not rental:
        raise NotFoundException()

    if data.inventory_id:
        inventory = inventory_service.get_by_id(data.inventory_id)
        if not inventory:
            raise NotFoundException("inventory not found")

    if data.customer_id:
        customer = customer_service.get_by_id(data.customer_id)
        if not customer:
            raise NotFoundException("customer not found")

    if data.staff_id:
        staff = staff_service.get_by_id(data.staff_id)
        if not staff:
            raise NotFoundException("staff not found")

    return rental_service.patch(rental_id, data)


@router.delete("/{rental_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rental_by_id(
    rental_service: Annotated[RentalService, Depends(RentalService)],
    rental_id: Annotated[int, Path(gt=0)],
):
    result = rental_service.delete(rental_id)
    if not result:
        raise NotFoundException()
