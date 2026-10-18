from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.language.service import LanguageService

from .schema import (
    CreateFilmSchema,
    FilmResponseSchema,
    PaginatedResponseSchema,
    PatchFilmSchema,
    UpdateFilmSchema,
)
from .service import FilmService

router = APIRouter(prefix="/films", tags=["Films"])


@router.get("/", response_model=PaginatedResponseSchema[FilmResponseSchema])
def get_all_films(
    film_service: Annotated[FilmService, Depends(FilmService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return film_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=FilmResponseSchema
)
def create_film(
    film_service: Annotated[FilmService, Depends(FilmService)],
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    data: CreateFilmSchema,
):
    language = language_service.get_by_id(data.language_id)
    if language is None:
        raise NotFoundException("language not found")

    return film_service.create(data)


@router.get("/{film_id}", response_model=FilmResponseSchema)
def get_film_by_id(
    film_service: Annotated[FilmService, Depends(FilmService)],
    film_id: Annotated[int, Path(gt=0)],
):
    film = film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException()

    return film


@router.patch("/{film_id}", response_model=FilmResponseSchema)
def patch_film_by_id(
    film_service: Annotated[FilmService, Depends(FilmService)],
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    film_id: Annotated[int, Path(gt=0)],
    data: PatchFilmSchema,
):

    if not data.language_id is None:
        language = language_service.get_by_id(data.language_id)
        if language is None:
            raise NotFoundException("language not found")

    film = film_service.patch(film_id, data)
    if not film:
        raise NotFoundException()

    return film


@router.put("/{film_id}", response_model=FilmResponseSchema)
def update_film_by_id(
    film_service: Annotated[FilmService, Depends(FilmService)],
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    film_id: Annotated[int, Path(gt=0)],
    data: UpdateFilmSchema,
):
    language = language_service.get_by_id(data.language_id)
    if language is None:
        raise NotFoundException("language not found")

    film = film_service.update(film_id, data)
    if not film:
        raise NotFoundException()

    return film


@router.delete("/{film_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_film_by_id(
    film_service: Annotated[FilmService, Depends(FilmService)],
    film_id: Annotated[int, Path(gt=0)],
):
    film = film_service.delete(film_id)
    if not film:
        raise NotFoundException()
