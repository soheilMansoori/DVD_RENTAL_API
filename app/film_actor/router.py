from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from app.actor.service import ActorService
from app.core.exceptions import NotFoundException
from app.film.service import FilmService

from .schema import FilmActorResponseSchema
from .service import FilmActorService

router = APIRouter(prefix="/films/{film_id}/actors", tags=["Film Actors"])


@router.get("/", response_model=list[FilmActorResponseSchema])
def get_film_actors(
    film_actor_service: Annotated[FilmActorService, Depends(FilmActorService)],
    film_service: Annotated[FilmService, Depends(FilmService)],
    film_id: Annotated[int, Path(gt=0)],
):
    film = film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException("film not found")

    return film_actor_service.get_actors_by_film(film_id)


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=FilmActorResponseSchema
)
def add_actor_to_film(
    film_actor_service: Annotated[FilmActorService, Depends(FilmActorService)],
    film_service: Annotated[FilmService, Depends(FilmService)],
    actor_service: Annotated[ActorService, Depends(ActorService)],
    film_id: Annotated[int, Path(gt=0)],
    actor_id: Annotated[int, Body(embed=True, gt=0)],
):

    film = film_service.get_by_id(film_id)
    if not film:
        raise NotFoundException("film not found")

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
