from math import ceil

from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from .model import Actor
from .schema import CreateActorSchema, PatchActorSchema, UpdateActorSchema


class ActorService:
    @staticmethod
    def search(
        db: Session,
        q: str,
        page: int = 1,
        size: int = 10,
    ):
        query = db.query(Actor).filter(
            or_(Actor.first_name.ilike(f"%{q}%"), Actor.last_name.ilike(f"%{q}%"))
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

    @staticmethod
    def get_all(
        db: Session,
        page: int = 1,
        size: int = 10,
    ):
        total = db.query(Actor).count()
        offset = (page - 1) * size
        items = db.query(Actor).limit(size).offset(offset).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    @staticmethod
    def get_by_id(db: Session, actor_id: int):
        return db.query(Actor).filter_by(id=actor_id).one_or_none()

    @staticmethod
    def create(db: Session, data: CreateActorSchema):
        new_actor = Actor(**data.model_dump())
        db.add(new_actor)
        db.commit()
        db.refresh(new_actor)
        return new_actor

    @staticmethod
    def update(db: Session, actor_id: int, data: UpdateActorSchema):
        actor = db.query(Actor).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(actor, key, value)

        db.commit()
        db.refresh(actor)
        return actor

    @staticmethod
    def patch(db: Session, actor_id: int, data: PatchActorSchema):
        actor = db.query(Actor).filter_by(id=actor_id).one_or_none()
        if not actor:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(actor, key, value)

        db.commit()
        db.refresh(actor)
        return actor

    @staticmethod
    def delete(db: Session, actor_id: int):
        actor = db.query(Actor).filter_by(id=actor_id).one_or_none()
        if actor:
            db.delete(actor)
            db.commit()
            return True
        return False
