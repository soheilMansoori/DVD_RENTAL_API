from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.address.service import AddressService
from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.store.service import StoreService

from .schema import (
    CreateStaffSchema,
    PaginatedResponseSchema,
    PatchStaffSchema,
    StaffResponseSchema,
    UpdatedStaffSchema,
)
from .service import StaffService

router = APIRouter(prefix="/staffs", tags=["Staffs"])


@router.get("/", response_model=PaginatedResponseSchema[StaffResponseSchema])
def get_all_staffs(
    staff_service: Annotated[StaffService, Depends(StaffService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return staff_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=StaffResponseSchema
)
def create_staff(
    staff_service: Annotated[StaffService, Depends(StaffService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    data: CreateStaffSchema,
):
    address = address_service.get_by_id(data.address_id)
    if not address:
        raise NotFoundException("address not found")

    store = store_service.get_by_id(data.store_id)
    if not store:
        raise NotFoundException("store not found")

    staff = staff_service.create(data)
    return staff


@router.get("/{staff_id}", response_model=StaffResponseSchema)
def get_staff_by_id(
    staff_service: Annotated[StaffService, Depends(StaffService)],
    staff_id: Annotated[int, Path(gt=0)],
):
    staff = staff_service.get_by_id(staff_id)
    if not staff:
        raise NotFoundException()

    return staff


@router.patch("/{staff_id}", response_model=StaffResponseSchema)
def patch_staff_by_id(
    staff_service: Annotated[StaffService, Depends(StaffService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    staff_id: Annotated[int, Path(gt=0)],
    data: PatchStaffSchema,
):
    staff = staff_service.get_by_id(staff_id)
    if not staff:
        raise NotFoundException()

    if data.address_id is not None:
        address = address_service.get_by_id(data.address_id)
        if not address:
            raise NotFoundException("address not found")

    if data.store_id is not None:
        store = store_service.get_by_id(data.store_id)
        if not store:
            raise NotFoundException("store not found")

    return staff_service.patch(staff_id, data)


@router.put("/{staff_id}", response_model=StaffResponseSchema)
def update_staff_by_id(
    staff_service: Annotated[StaffService, Depends(StaffService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    staff_id: Annotated[int, Path(gt=0)],
    data: UpdatedStaffSchema,
):
    staff = staff_service.get_by_id(staff_id)
    if not staff:
        raise NotFoundException()

    address = address_service.get_by_id(data.address_id)
    if not address:
        raise NotFoundException("address not found")

    store = store_service.get_by_id(data.store_id)
    if not store:
        raise NotFoundException("store not found")

    return staff_service.update(staff_id, data)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff_by_id(
    staff_service: Annotated[StaffService, Depends(StaffService)],
    staff_id: Annotated[int, Path(gt=0)],
):
    result = staff_service.delete(staff_id)
    if not result:
        raise NotFoundException()
