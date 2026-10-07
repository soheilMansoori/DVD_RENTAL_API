from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
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
    db: Annotated[Session, Depends(get_db)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return ActorService.get_all(db, page=page, size=size)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ActorResponseSchema
)
def create_actor(db: Annotated[Session, Depends(get_db)], data: CreateActorSchema):
    return ActorService.create(db, data)


@router.get("/{actor_id}", response_model=ActorResponseSchema)
def get_actor_by_id(
    db: Annotated[Session, Depends(get_db)],
    actor_id: Annotated[int, Path(gt=0)],
):
    actor = ActorService.get_by_id(db, actor_id)
    if not actor:
        raise NotFoundException()

    return actor


@router.patch("/{actor_id}", response_model=ActorResponseSchema)
def patch_actor_by_id(
    actor_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    data: PatchActorSchema,
):
    actor = ActorService.patch(db, actor_id, data)
    if not actor:
        raise NotFoundException()
    return actor


@router.put("/{actor_id}", response_model=ActorResponseSchema)
def update_actor_by_id(
    actor_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
    data: UpdateActorSchema,
):
    actor = ActorService.update(db, actor_id, data)
    if not actor:
        raise NotFoundException()
    return actor


@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor_by_id(
    actor_id: Annotated[int, Path(gt=0)],
    db: Annotated[Session, Depends(get_db)],
):
    actor = ActorService.delete(db, actor_id)
    if not actor:
        raise NotFoundException()


@router.get("/search", response_model=PaginatedResponseSchema[ActorResponseSchema])
def search_actors(
    db: Annotated[Session, Depends(get_db)],
    q: Annotated[str, Query(..., min_length=1)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return ActorService.search(db, page=page, size=size, q=q)
