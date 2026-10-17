from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException

from .schema import (
    CreateLanguageSchema,
    LanguageResponseSchema,
    PaginatedResponseSchema,
)
from .service import LanguageService

router = APIRouter(prefix="/languages", tags=["Languages"])


@router.get("/", response_model=PaginatedResponseSchema[LanguageResponseSchema])
def get_all_languages(
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return language_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=LanguageResponseSchema
)
def create_language(
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    data: CreateLanguageSchema,
):
    return language_service.create(data)


@router.get("/{language_id}", response_model=LanguageResponseSchema)
def get_language_by_id(
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    language_id: Annotated[int, Path(..., gt=0)],
):
    language = language_service.get_by_id(language_id)
    if not language:
        raise NotFoundException()
    return language


@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language_by_id(
    language_service: Annotated[LanguageService, Depends(LanguageService)],
    language_id: Annotated[int, Path(..., gt=0)],
):
    language = language_service.delete(language_id)
    if not language:
        raise NotFoundException()
