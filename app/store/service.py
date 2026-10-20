from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db

from .model import Store
from .schema import CreateStoreSchema, PatchStoreSchema, UpdateStoreSchema


class StoreService:
    db: Session
    model: type[Store] = Store

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_all(self, pagination: Pagination):
        page, size = (pagination.page, pagination.size)
        model = self.model
        query = self.db.query(model)

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

    def get_by_id(self, store_id: int):
        return self.db.query(self.model).filter_by(id=store_id).one_or_none()

    def create(self, data: CreateStoreSchema):
        db, model = (self.db, self.model)

        new_store = model(**data.model_dump())
        db.add(new_store)
        db.commit()
        db.refresh(new_store)

        return new_store

    def update(self, store_id: int, data: UpdateStoreSchema):
        db, model = (self.db, self.model)
        store = db.query(model).filter_by(id=store_id).one_or_none()
        if not store:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(store, key, value)

        db.commit()
        db.refresh(store)
        return store

    def patch(self, store_id: int, data: PatchStoreSchema):
        db, model = (self.db, self.model)
        store = db.query(model).filter_by(id=store_id).one_or_none()
        if not store:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(store, key, value)

        db.commit()
        db.refresh(store)
        return store

    def delete(self, store_id: int):
        db, model = (self.db, self.model)
        store = db.query(model).filter_by(id=store_id).one_or_none()
        if store:
            db.delete(store)
            db.commit()
            return True

        return False

    def is_address_in_store(self, address_id: int):
        db, model = self.db, self.model
        exists = db.query(model).filter(model.address_id == address_id).one_or_none()
        return exists is not None
