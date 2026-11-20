from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Store
from .schema import (
    CreateStoreSchema,
    PatchStoreSchema,
    StoreFiltersSchema,
    UpdateStoreSchema,
)


class StoreService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Store

    def get_all(
        self, pagination: Pagination, filters: StoreFiltersSchema
    ) -> PaginatedResponseSchema[Store]:
        query = self.db.query(self.model)

        if filters.manager_staff_id:
            query = query.filter(
                self.model.manager_staff_id == filters.manager_staff_id
            )

        if filters.address_id:
            query = query.filter(self.model.address_id == filters.address_id)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.offset(offset).limit(pagination.size).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, store_id: int) -> Store | None:
        return self.db.query(self.model).filter_by(id=store_id).one_or_none()

    def create(self, data: CreateStoreSchema) -> Store:
        new_store = self.model(**data.model_dump())
        self.db.add(new_store)
        self.db.commit()
        self.db.refresh(new_store)
        return new_store

    def update(self, store_id: int, data: UpdateStoreSchema) -> Store | None:
        store = self.db.query(self.model).filter_by(id=store_id).one_or_none()
        if not store:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(store, key, value)

        self.db.commit()
        self.db.refresh(store)
        return store

    def patch(self, store_id: int, data: PatchStoreSchema) -> Store | None:
        store = self.db.query(self.model).filter_by(id=store_id).one_or_none()
        if not store:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(store, key, value)

        self.db.commit()
        self.db.refresh(store)
        return store

    def delete(self, store_id: int) -> Store | None:
        store = self.db.query(self.model).filter_by(id=store_id).one_or_none()
        if not store:
            return None

        self.db.delete(store)
        self.db.commit()
        return store

    def is_address_in_store(self, address_id: int) -> bool:
        exists = (
            self.db.query(self.model)
            .filter(self.model.address_id == address_id)
            .one_or_none()
        )
        return exists is not None
