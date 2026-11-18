from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from app.actor.service import ActorService
from app.core.dependencies import Pagination
from app.core.exceptions import NotFoundException
from app.core.schemas import PaginatedResponseSchema
from app.film.service import FilmService

from .schema import FilmActorResponseSchema
from .service import FilmActorService


# check film exists dependence
def check_film_exists(
    film_id: Annotated[int, Path(gt=0)],
    film_service: Annotated[FilmService, Depends(FilmService)],
):
    film = film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException("film not found")

    return film


router = APIRouter(
    prefix="/films/{film_id}/actors",
    dependencies=[Depends(check_film_exists)],
    tags=["Film Actors"],
)


@router.get("/", response_model=PaginatedResponseSchema[FilmActorResponseSchema])
def get_film_actors(
    film_actor_service: Annotated[FilmActorService, Depends(FilmActorService)],
    film_id: Annotated[int, Path(gt=0)],
    pagination: Annotated[Pagination, Depends(Pagination)],
):

    return film_actor_service.get_actors_by_film(film_id, pagination)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=FilmActorResponseSchema
)
def add_actor_to_film(
    film_actor_service: Annotated[FilmActorService, Depends(FilmActorService)],
    actor_service: Annotated[ActorService, Depends(ActorService)],
    film_id: Annotated[int, Path(gt=0)],
    actor_id: Annotated[int, Body(embed=True, gt=0)],
):

    actor = actor_service.get_by_id(actor_id)
    if not actor:
        raise NotFoundException("actor not found")

    if film_actor_service.is_actor_in_film(film_id, actor_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="this actor is already assigned to this film",
        )

    return film_actor_service.add_actor_to_film(film_id, actor_id)


@router.delete("/{actor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_actor_from_film(
    film_actor_service: Annotated[FilmActorService, Depends(FilmActorService)],
    film_id: Annotated[int, Path(gt=0)],
    actor_id: Annotated[int, Path(gt=0)],
):
    result = film_actor_service.delete_actor_from_film(film_id, actor_id)
    if not result:
        raise NotFoundException("relation not found")
