from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from app.core.dependencies import Pagination, get_db

from .model import Actor
from .schema import CreateActorSchema, PatchActorSchema, UpdateActorSchema


class ActorService:
    db: Session
    model: type[Actor] = Actor

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_all(self, pagination: Pagination):
        page, size, q = (pagination.page, pagination.size, pagination.q)
        model = self.model
        query = self.db.query(model)

        if not q is None:
            query = query.filter(
                or_(
                    model.first_name.ilike(f"%{q}%"),
                    model.last_name.ilike(f"%{q}%"),
                )
            )

        total = query.count()
        offset = (page - 1) * size
        items = query.offset(offset).limit(size).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    def get_by_id(self, actor_id: int):
        return self.db.query(self.model).filter_by(id=actor_id).one_or_none()

    def create(self, data: CreateActorSchema):
        db, model = (self.db, self.model)

        new_actor = model(**data.model_dump())
        db.add(new_actor)
        db.commit()
        db.refresh(new_actor)

        return new_actor

    def update(self, actor_id: int, data: UpdateActorSchema):
        db, model = (self.db, self.model)
        actor = db.query(model).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(actor, key, value)

        db.commit()
        db.refresh(actor)
        return actor

    def patch(self, actor_id: int, data: PatchActorSchema):
        db, model = (self.db, self.model)
        actor = db.query(model).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(actor, key, value)

        db.commit()
        db.refresh(actor)
        return actor

    def delete(self, actor_id: int):
        db, model = (self.db, self.model)
        actor = db.query(model).filter_by(id=actor_id).one_or_none()
        if actor:
            db.delete(actor)
            db.commit()
            return True

        return False
