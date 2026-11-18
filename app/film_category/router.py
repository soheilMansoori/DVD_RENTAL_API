from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from app.category.service import CategoryService
from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.core.schemas import PaginatedResponseSchema
from app.film.service import FilmService

from .schema import FilmCategoryResponseSchema
from .service import FilmCategoryService


def check_film_exists(
    film_id: Annotated[int, Path(gt=0)],
    film_service: Annotated[FilmService, Depends(FilmService)],
):
    film = film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException("film not found")

    return film


router = APIRouter(
    prefix="/films/{film_id}/categories",
    dependencies=[Depends(check_film_exists)],
    tags=["Film Categories"],
)


@router.get("/", response_model=PaginatedResponseSchema[FilmCategoryResponseSchema])
def get_film_categories(
    film_id: Annotated[int, Path(gt=0)],
    pagination: Annotated[Pagination, Depends(Pagination)],
    film_category_service: Annotated[FilmCategoryService, Depends(FilmCategoryService)],
):
    return film_category_service.get_categories_by_film(film_id, pagination)


@router.post(
    "/", response_model=FilmCategoryResponseSchema, status_code=status.HTTP_201_CREATED
)
def add_category_to_film(
    film_id: Annotated[int, Path(gt=0)],
    category_id: Annotated[int, Body(embed=True, gt=0)],
    category_service: Annotated[CategoryService, Depends(CategoryService)],
    film_category_service: Annotated[FilmCategoryService, Depends(FilmCategoryService)],
):
    category = category_service.get_by_id(category_id)

    if not category:
        raise NotFoundException("category not found")

    if film_category_service.is_category_in_film(film_id, category_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="this category is already assigned to this film",
        )

    return film_category_service.add_category_to_film(film_id, category_id)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_from_film(
    film_id: Annotated[int, Path(gt=0)],
    category_id: Annotated[int, Path(gt=0)],
    category_service: Annotated[CategoryService, Depends()],
    film_category_service: Annotated[FilmCategoryService, Depends()],
):
    category = category_service.get_by_id(category_id)

    if not category:
        raise NotFoundException("category not found")

    result = film_category_service.delete_category_from_film(film_id, category_id)

    if not result:
        raise NotFoundException("category is not assigned to this film")
