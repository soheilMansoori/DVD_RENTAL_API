from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Rental
from .schema import CreateRentalSchema, PatchRentalSchema, RentalFiltersSchema


class RentalService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Rental

    def get_all(
        self, pagination: Pagination, filters: RentalFiltersSchema
    ) -> PaginatedResponseSchema[Rental]:
        query = self.db.query(self.model)

        if filters.inventory_id:
            query = query.filter(self.model.inventory_id == filters.inventory_id)

        if filters.customer_id:
            query = query.filter(self.model.customer_id == filters.customer_id)

        if filters.staff_id:
            query = query.filter(self.model.staff_id == filters.staff_id)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = (
            query.order_by(self.model.id.desc())
            .offset(offset)
            .limit(pagination.size)
            .all()
        )

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, rental_id: int) -> Rental | None:
        return self.db.query(self.model).filter_by(id=rental_id).one_or_none()

    def create(self, data: CreateRentalSchema) -> Rental:
        rental = self.model(**data.model_dump())
        self.db.add(rental)
        self.db.commit()
        self.db.refresh(rental)
        return rental

    def patch(self, rental_id: int, data: PatchRentalSchema) -> Rental | None:
        rental = self.get_by_id(rental_id)
        if not rental:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(rental, key, value)

        self.db.commit()
        self.db.refresh(rental)
        return rental

    def update(self, rental_id: int, data: UpdateRentalSchema) -> Rental | None:
        rental = self.get_by_id(rental_id)
        if not rental:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(rental, key, value)

        self.db.commit()
        self.db.refresh(rental)
        return rental

    def delete(self, rental_id: int) -> Rental | None:
        rental = self.get_by_id(rental_id)
        if not rental:
            return None

        self.db.delete(rental)
        self.db.commit()
        return rental
