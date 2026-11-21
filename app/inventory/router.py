from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.core.schemas import PaginatedResponseSchema
from app.film.service import FilmService
from app.store.service import StoreService

from .schema import (
    CreateInventorySchema,
    InventoryFiltersSchema,
    InventoryResponseSchema,
)
from .service import InventoryService

router = APIRouter(prefix="/inventories", tags=["Inventories"])


@router.get("/", response_model=PaginatedResponseSchema[InventoryResponseSchema])
def get_all_inventories(
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
    filters: Annotated[InventoryFiltersSchema, Depends(InventoryFiltersSchema)],
):
    return inventory_service.get_all(pagination, filters)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=InventoryResponseSchema
)
def create_inventory(
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    film_service: Annotated[FilmService, Depends(FilmService)],
    store_service: Annotated[StoreService, Depends(StoreService)],
    data: CreateInventorySchema,
):
    # validate film
    film = film_service.get_by_id(data.film_id)
    if not film:
        raise NotFoundException("film not found")

    # validate store
    store = store_service.get_by_id(data.store_id)
    if not store:
        raise NotFoundException("store not found")

    return inventory_service.create(data)


@router.get("/{inventory_id}", response_model=InventoryResponseSchema)
def get_inventory_by_id(
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    inventory_id: Annotated[int, Path(gt=0)],
):
    inventory = inventory_service.get_by_id(inventory_id)
    if not inventory:
        raise NotFoundException()
    return inventory


@router.delete("/{inventory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_by_id(
    inventory_service: Annotated[InventoryService, Depends(InventoryService)],
    inventory_id: Annotated[int, Path(gt=0)],
):
    result = inventory_service.delete(inventory_id)
    if not result:
        raise NotFoundException()
