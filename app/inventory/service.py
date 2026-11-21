from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Inventory
from .schema import CreateInventorySchema, InventoryFiltersSchema


class InventoryService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Inventory

    def get_all(
        self, pagination: Pagination, filters: InventoryFiltersSchema
    ) -> PaginatedResponseSchema[Inventory]:
        query = self.db.query(self.model)

        if filters.film_id:
            query = query.filter(self.model.film_id == filters.film_id)

        if filters.store_id:
            query = query.filter(self.model.store_id == filters.store_id)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = (
            query.order_by(self.model.id).offset(offset).limit(pagination.size).all()
        )

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, inventory_id: int) -> Inventory | None:
        return self.db.query(self.model).filter_by(id=inventory_id).one_or_none()

    def create(self, data: CreateInventorySchema) -> Inventory:
        inventory = self.model(**data.model_dump())
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(inventory)
        return inventory

    def delete(self, inventory_id: int) -> Inventory | None:
        inventory = self.get_by_id(inventory_id)
        if not inventory:
            return None

        self.db.delete(inventory)
        self.db.commit()
        return inventory
