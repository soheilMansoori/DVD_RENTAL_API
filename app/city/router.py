from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.country.service import CountryService

from .schema import CityResponseSchema, CreateCitySchema, PaginatedResponseSchema
from .service import CityService

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/", response_model=PaginatedResponseSchema[CityResponseSchema])
def get_all_cities(
    city_service: Annotated[CityService, Depends(CityService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return city_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CityResponseSchema
)
def create_city(
    city_service: Annotated[CityService, Depends(CityService)],
    country_service: Annotated[CountryService, Depends(CountryService)],
    data: CreateCitySchema,
):
    result = country_service.get_by_id(data.country_id)
    if result is None:
        raise NotFoundException("country not found")

    return city_service.create(data)


@router.get("/{city_id}", response_model=CityResponseSchema)
def get_city_by_id(
    city_service: Annotated[CityService, Depends(CityService)],
    city_id: Annotated[int, Path(gt=0)],
):
    city = city_service.get_by_id(city_id)
    if city is None:
        raise NotFoundException()

    return city


@router.delete("/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city_by_id(
    city_service: Annotated[CityService, Depends(CityService)],
    city_id: Annotated[int, Path(gt=0)],
):
    city = city_service.delete(city_id)
    if city is None:
        raise NotFoundException()
