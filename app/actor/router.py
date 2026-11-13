from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException

from .schema import (
    ActorResponseSchema,
    CreateActorSchema,
    PaginatedResponseSchema,
    PatchActorSchema,
    UpdateActorSchema,
)
from .service import ActorService

router = APIRouter(prefix="/actors", tags=["Actors"])


@router.get("/", response_model=PaginatedResponseSchema[ActorResponseSchema])
def get_all_actors(
    actor_service: Annotated[ActorService, Depends(ActorService)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):
    return actor_service.get_all(pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ActorResponseSchema
)
def create_actor(
    actor_service: Annotated[ActorService, Depends(ActorService)],
    data: CreateActorSchema,
):
    return actor_service.create(data)


@router.get("/{actor_id}", response_model=ActorResponseSchema)
def get_actor_by_id(
    actor_service: Annotated[ActorService, Depends(ActorService)],
    actor_id: Annotated[int, Path(gt=0)],
):
    actor = actor_service.get_by_id(actor_id)
    if not actor:
        raise NotFoundException()

    return actor


@router.patch("/{actor_id}", response_model=ActorResponseSchema)
def patch_actor_by_id(
    actor_service: Annotated[ActorService, Depends(ActorService)],
    actor_id: Annotated[int, Path(gt=0)],
    data: PatchActorSchema,
):
    actor = actor_service.patch(actor_id, data)
    if not actor:
        raise NotFoundException()
    return actor


@router.put("/{actor_id}", response_model=ActorResponseSchema)
def update_actor_by_id(
    actor_service: Annotated[ActorService, Depends(ActorService)],
    actor_id: Annotated[int, Path(gt=0)],
    data: UpdateActorSchema,
):
    actor = actor_service.update(actor_id, data)
    if not actor:
        raise NotFoundException()
    return actor


@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor_by_id(
    actor_service: Annotated[ActorService, Depends(ActorService)],
    actor_id: Annotated[int, Path(gt=0)],
):
    actor = actor_service.delete(actor_id)
    if not actor:
        raise NotFoundException()
