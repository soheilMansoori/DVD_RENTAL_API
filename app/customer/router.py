from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.address.service import AddressService
from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.store.service import StoreService

from .schema import (
    CreateCustomerSchema,
    CustomerResponseSchema,
    PaginatedResponseSchema,
    PatchCustomerSchema,
    UpdatedCustomerSchema,
)
from .service import CustomerService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=PaginatedResponseSchema[CustomerResponseSchema])
def get_all_customers(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return customer_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CustomerResponseSchema
)
def create_customer(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    data: CreateCustomerSchema,
):
    address = address_service.get_by_id(data.address_id)
    if not address:
        raise NotFoundException("address not found")

    store = store_service.get_by_id(data.store_id)
    if not store:
        raise NotFoundException("store not found")

    customer = customer_service.create(data)
    return customer


@router.get("/{customer_id}", response_model=CustomerResponseSchema)
def get_customer_by_id(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    customer_id: Annotated[int, Path(gt=0)],
):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise NotFoundException()

    return customer


@router.patch("/{customer_id}", response_model=CustomerResponseSchema)
def patch_customer_by_id(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    customer_id: Annotated[int, Path(gt=0)],
    data: PatchCustomerSchema,
):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise NotFoundException()

    if data.address_id is not None:
        address = address_service.get_by_id(data.address_id)
        if not address:
            raise NotFoundException("address not found")

    if data.store_id is not None:
        store = store_service.get_by_id(data.store_id)
        if not store:
            raise NotFoundException("store not found")

    return customer_service.patch(customer_id, data)


@router.put("/{customer_id}", response_model=CustomerResponseSchema)
def update_customer_by_id(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    customer_id: Annotated[int, Path(gt=0)],
    data: UpdatedCustomerSchema,
):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise NotFoundException()

    address = address_service.get_by_id(data.address_id)
    if not address:
        raise NotFoundException("address not found")

    store = store_service.get_by_id(data.store_id)
    if not store:
        raise NotFoundException("store not found")

    return customer_service.update(customer_id, data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer_by_id(
    customer_service: Annotated[CustomerService, Depends(CustomerService)],
    customer_id: Annotated[int, Path(gt=0)],
):
    result = customer_service.delete(customer_id)
    if not result:
        raise NotFoundException()
