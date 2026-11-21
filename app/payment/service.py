from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Payment
from .schema import (
    CreatePaymentSchema,
    PatchPaymentSchema,
    PaymentFiltersSchema,
    UpdatePaymentSchema,
)


class PaymentService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Payment

    def get_all(
        self, pagination: Pagination, filters: PaymentFiltersSchema
    ) -> PaginatedResponseSchema[Payment]:
        query = self.db.query(self.model)

        if filters.customer_id is not None:
            query = query.filter(self.model.customer_id == filters.customer_id)

        if filters.staff_id is not None:
            query = query.filter(self.model.staff_id == filters.staff_id)

        if filters.rental_id is not None:
            query = query.filter(self.model.rental_id == filters.rental_id)

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

    def get_by_id(self, payment_id: int) -> Payment | None:
        return self.db.query(self.model).filter_by(id=payment_id).one_or_none()

    def create(self, data: CreatePaymentSchema) -> Payment:
        payment = self.model(**data.model_dump())
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def update(self, payment_id: int, data: UpdatePaymentSchema) -> Payment | None:
        payment = self.get_by_id(payment_id)
        if not payment:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(payment, key, value)

        self.db.commit()
        self.db.refresh(payment)
        return payment

    def patch(self, payment_id: int, data: PatchPaymentSchema) -> Payment | None:
        payment = self.get_by_id(payment_id)
        if not payment:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(payment, key, value)

        self.db.commit()
        self.db.refresh(payment)
        return payment

    def delete(self, payment_id: int) -> Payment | None:
        payment = self.get_by_id(payment_id)
        if not payment:
            return None

        self.db.delete(payment)
        self.db.commit()
        return payment
