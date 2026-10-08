from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.exceptions import NotFoundException

from .schema import CountryResponseSchema, CreateCountrySchema, PaginatedResponseSchema
from .service import CountryService

router = APIRouter(prefix="/countries", tags=["Countries"])


@router.get("/", response_model=PaginatedResponseSchema[CountryResponseSchema])
def get_all_countries(
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return CountryService.get_all(db, page=page, size=size)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CountryResponseSchema
)
def create_country(db: Annotated[Session, Depends(get_db)], data: CreateCountrySchema):
    return CountryService.create(db, data)


@router.delete("/{country_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country_by_id(
    db: Annotated[Session, Depends(get_db)], country_id: Annotated[int, Path(..., gt=0)]
):
    country = CountryService.delete(db, country_id)
    if not country:
        raise NotFoundException()
