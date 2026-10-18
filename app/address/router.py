from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.city.service import CityService
from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException

from .schema import (
    AddressResponseSchema,
    CreateAddressSchema,
    PaginatedResponseSchema,
    PatchAddressSchema,
    UpdateAddressSchema,
)
from .service import AddressService

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/", response_model=PaginatedResponseSchema[AddressResponseSchema])
def get_all_addresses(
    address_service: Annotated[AddressService, Depends(AddressService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return address_service.get_all(pagination)


@router.post(
    "/", response_model=AddressResponseSchema, status_code=status.HTTP_201_CREATED
)
def create_address(
    address_service: Annotated[AddressService, Depends(AddressService)],
    city_service: Annotated[CityService, Depends(CityService)],
    data: CreateAddressSchema,
):
    city = city_service.get_by_id(data.city_id)
    if city is None:
        raise NotFoundException("city not found")

    return address_service.create(data)


@router.get("/{address_id}", response_model=AddressResponseSchema)
def get_address_by_id(
    address_service: Annotated[AddressService, Depends(AddressService)],
    address_id: int = Path(gt=0),
):
    address = address_service.get_by_id(address_id)
    if address is None:
        raise NotFoundException()

    return address


@router.put("/{address_id}", response_model=AddressResponseSchema)
def update_address_by_id(
    data: UpdateAddressSchema,
    address_service: Annotated[AddressService, Depends(AddressService)],
    city_service: Annotated[CityService, Depends(CityService)],
    address_id: int = Path(gt=0),
):
    address = address_service.get_by_id(address_id)
    if address is None:
        raise NotFoundException()

    city = city_service.get_by_id(data.city_id)
    if city is None:
        raise NotFoundException("city not found")

    return address_service.update(address_id, data)


@router.patch("/{address_id}", response_model=AddressResponseSchema)
def patch_address_by_id(
    data: PatchAddressSchema,
    address_service: Annotated[AddressService, Depends(AddressService)],
    city_service: Annotated[CityService, Depends(CityService)],
    address_id: int = Path(gt=0),
):
    address = address_service.get_by_id(address_id)
    if address is None:
        raise NotFoundException()

    if not data.city_id is None:
        city = city_service.get_by_id(data.city_id)
        if city is None:
            raise NotFoundException("city not found")

    return address_service.patch(address_id, data)


@router.delete(
    "/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_address_by_id(
    address_service: Annotated[AddressService, Depends(AddressService)],
    address_id: int = Path(gt=0),
):
    address = address_service.delete(address_id)
    if address is None:
        raise NotFoundException()
