from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException

from .schema import (
    CategoryResponseSchema,
    CreateCategorySchema,
    PaginatedResponseSchema,
)
from .service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=PaginatedResponseSchema[CategoryResponseSchema])
def get_all_categories(
    category_service: Annotated[CategoryService, Depends(CategoryService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return category_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponseSchema
)
def create_category(
    category_service: Annotated[CategoryService, Depends(CategoryService)],
    data: CreateCategorySchema,
):

    return category_service.create(data)


@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category_by_id(
    category_service: Annotated[CategoryService, Depends(CategoryService)],
    category_id: Annotated[int, Path(gt=0)],
):
    category = category_service.get_by_id(category_id)
    if category is None:
        raise NotFoundException()

    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_by_id(
    category_service: Annotated[CategoryService, Depends(CategoryService)],
    category_id: Annotated[int, Path(gt=0)],
):
    category = category_service.delete(category_id)
    if category is None:
        raise NotFoundException()
