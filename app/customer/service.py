from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from app.core.dependencies import Pagination, get_db

from .model import Customer
from .schema import (
    CreateCustomerSchema,
    PatchCustomerSchema,
    UpdatedCustomerSchema,
)


class CustomerService:
    db: Session
    model: type[Customer] = Customer

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
                    model.email.ilike(f"%{q}%"),
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

    def get_by_id(self, customer_id: int):
        return self.db.query(self.model).filter_by(id=customer_id).one_or_none()

    def create(self, data: CreateCustomerSchema):
        db, model = (self.db, self.model)

        new_customer = model(**data.model_dump())
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return new_customer

    def update(self, customer_id: int, data: UpdatedCustomerSchema):
        db, model = (self.db, self.model)
        customer = db.query(model).filter_by(id=customer_id).one_or_none()
        if not customer:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)
        return customer

    def patch(self, customer_id: int, data: PatchCustomerSchema):
        db, model = (self.db, self.model)
        customer = db.query(model).filter_by(id=customer_id).one_or_none()
        if not customer:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(customer, key, value)

        db.commit()
        db.refresh(customer)
        return customer

    def delete(self, customer_id: int):
        db, model = (self.db, self.model)
        customer = db.query(model).filter_by(id=customer_id).one_or_none()
        if customer:
            db.delete(customer)
            db.commit()
            return True

        return False
