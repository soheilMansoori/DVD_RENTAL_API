from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
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
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return LanguageService.get_all(db, page=page, size=size)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=LanguageResponseSchema
)
def create_language(
    db: Annotated[Session, Depends(get_db)], data: CreateLanguageSchema
):
    return LanguageService.create(db, data)


@router.delete("/{language_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language_by_id(
    db: Annotated[Session, Depends(get_db)],
    language_id: Annotated[int, Path(..., gt=0)],
):
    language = LanguageService.delete(db, language_id)
    if not language:
        raise NotFoundException()
