from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from app.address.service import AddressService
from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException

from .schema import (
    CreateStoreSchema,
    PaginatedResponseSchema,
    PatchStoreSchema,
    StoreResponseSchema,
    UpdateStoreSchema,
)
from .service import StoreService

router = APIRouter(prefix="/stores", tags=["Stores"])


@router.get("/", response_model=PaginatedResponseSchema[StoreResponseSchema])
def get_all_stores(
    store_service: Annotated[StoreService, Depends(StoreService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return store_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=StoreResponseSchema
)
def create_store(
    store_service: Annotated[StoreService, Depends(StoreService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    data: CreateStoreSchema,
):
    address = address_service.get_by_id(data.address_id)
    if not address:
        raise NotFoundException("address not found")

    # TODO: check staff.id from staff service

    return store_service.create(data)


@router.get("/{store_id}", response_model=StoreResponseSchema)
def get_store_by_id(
    store_service: Annotated[StoreService, Depends(StoreService)],
    store_id: Annotated[int, Path(gt=0)],
):
    store = store_service.get_by_id(store_id)

    if not store:
        raise NotFoundException()

    return store


@router.patch("/{store_id}", response_model=StoreResponseSchema)
def patch_store_by_id(
    store_service: Annotated[StoreService, Depends(StoreService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_id: Annotated[int, Path(gt=0)],
    data: PatchStoreSchema,
):
    store = store_service.get_by_id(store_id)

    if not store:
        raise NotFoundException()

    if data.address_id is not None:
        address = address_service.get_by_id(data.address_id)
        if not address:
            raise NotFoundException("address not found")

    # TODO: check staff.id from staff service

    return store_service.patch(store_id, data)


@router.put("/{store_id}", response_model=StoreResponseSchema)
def update_store_by_id(
    store_service: Annotated[StoreService, Depends(StoreService)],
    address_service: Annotated[AddressService, Depends(AddressService)],
    store_id: Annotated[int, Path(gt=0)],
    data: UpdateStoreSchema,
):

    store = store_service.get_by_id(store_id)

    if not store:
        raise NotFoundException()

    address = address_service.get_by_id(data.address_id)
    if not address:
        raise NotFoundException("address not found")

    if store_service.is_address_in_store(data.address_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="this address is already assigned to this store",
        )

    # TODO: check staff.id from staff service

    return store_service.update(store_id, data)


@router.delete("/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store_by_id(
    store_service: Annotated[StoreService, Depends(StoreService)],
    store_id: Annotated[int, Path(gt=0)],
):
    result = store_service.delete(store_id)
    if not result:
        raise NotFoundException()
