from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException

from .schema import CountryResponseSchema, CreateCountrySchema, PaginatedResponseSchema
from .service import CountryService

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", response_model=PaginatedResponseSchema[CountryResponseSchema])
def get_all_countries(
    country_service: Annotated[CountryService, Depends(CountryService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return country_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CountryResponseSchema
)
def create_country(
    country_service: Annotated[CountryService, Depends(CountryService)],
    data: CreateCountrySchema,
):
    return country_service.create(data)


@router.get("/{country_id}", response_model=CountryResponseSchema)
def get_country_by_id(
    country_service: Annotated[CountryService, Depends(CountryService)],
    country_id: Annotated[int, Path(..., gt=0)],
):
    country = country_service.get_by_id(country_id)
    if not country:
        raise NotFoundException()
    return country


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country_by_id(
    country_service: Annotated[CountryService, Depends(CountryService)],
    country_id: Annotated[int, Path(..., gt=0)],
):
    country = country_service.delete(country_id)
    if not country:
        raise NotFoundException()
