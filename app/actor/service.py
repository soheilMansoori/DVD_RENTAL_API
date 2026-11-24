from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Actor
from .schema import (
    ActorFiltersSchema,
    CreateActorSchema,
    PatchActorSchema,
    UpdateActorSchema,
)


class ActorService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db
        self.model = Actor

    def get_all(
        self, pagination: Pagination, filters: ActorFiltersSchema
    ) -> PaginatedResponseSchema[Actor]:
        query = self.db.query(self.model)

        if filters.first_name:
            query = query.filter(self.model.first_name.ilike(f"%{filters.first_name}%"))

        if filters.last_name:
            query = query.filter(self.model.last_name.ilike(f"%{filters.last_name}%"))

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.offset(offset).limit(pagination.size).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, actor_id: int) -> Actor | None:
        return self.db.query(self.model).filter_by(id=actor_id).one_or_none()

    def create(self, data: CreateActorSchema) -> Actor:
        new_actor = self.model(**data.model_dump())

        self.db.add(new_actor)
        self.db.commit()
        self.db.refresh(new_actor)

        return new_actor

    def update(self, actor_id: int, data: UpdateActorSchema) -> Actor | None:
        actor = self.db.query(self.model).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(actor, key, value)

        self.db.commit()
        self.db.refresh(actor)

        return actor

    def patch(self, actor_id: int, data: PatchActorSchema) -> Actor | None:
        actor = self.db.query(self.model).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(actor, key, value)

        self.db.commit()
        self.db.refresh(actor)
        return actor

    def delete(self, actor_id: int) -> Actor | None:
        actor = self.db.query(self.model).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        self.db.delete(actor)
        self.db.commit()
        return actor
