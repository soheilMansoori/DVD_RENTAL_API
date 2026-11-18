from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Customer
from .schema import (
    CreateCustomerSchema,
    CustomerFiltersSchema,
    PatchCustomerSchema,
    UpdatedCustomerSchema,
)


class CustomerService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Customer

    def get_all(
        self, pagination: Pagination, filters: CustomerFiltersSchema
    ) -> PaginatedResponseSchema[Customer]:
        query = self.db.query(self.model)

        if filters.first_name:
            query = query.filter(self.model.first_name.ilike(f"%{filters.first_name}%"))

        if filters.last_name:
            query = query.filter(self.model.last_name.ilike(f"%{filters.last_name}%"))

        if filters.email:
            query = query.filter(self.model.email.ilike(f"%{filters.email}%"))

        if filters.store_id:
            query = query.filter_by(store_id=filters.store_id)

        if filters.address_id:
            query = query.filter_by(address_id=filters.address_id)

        if filters.active is not None:
            query = query.filter_by(active=filters.active)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.offset(offset).limit(pagination.size).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.db.query(self.model).filter_by(id=customer_id).one_or_none()

    def create(self, data: CreateCustomerSchema) -> Customer:
        new_customer = self.model(**data.model_dump())
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def update(self, customer_id: int, data: UpdatedCustomerSchema) -> Customer | None:
        customer = self.db.query(self.model).filter_by(id=customer_id).one_or_none()
        if not customer:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)
        return customer

    def patch(self, customer_id: int, data: PatchCustomerSchema) -> Customer | None:
        customer = self.db.query(self.model).filter_by(id=customer_id).one_or_none()
        if not customer:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer, key, value)

        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer_id: int) -> Customer | None:
        customer = self.db.query(self.model).filter_by(id=customer_id).one_or_none()
        if not customer:
            return None

        self.db.delete(customer)
        self.db.commit()
        return customer
