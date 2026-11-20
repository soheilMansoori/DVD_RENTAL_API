from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Staff
from .schema import (
    CreateStaffSchema,
    PatchStaffSchema,
    StaffFiltersSchema,
    UpdatedStaffSchema,
)


class StaffService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Staff

    def get_all(
        self, pagination: Pagination, filters: StaffFiltersSchema
    ) -> PaginatedResponseSchema[Staff]:
        query = self.db.query(self.model)

        if filters.first_name:
            query = query.filter(self.model.first_name.ilike(f"%{filters.first_name}%"))

        if filters.last_name:
            query = query.filter(self.model.last_name.ilike(f"%{filters.last_name}%"))

        if filters.email:
            query = query.filter(self.model.email.ilike(f"%{filters.email}%"))

        if filters.username:
            query = query.filter(self.model.username.ilike(f"%{filters.username}%"))

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

    def get_by_id(self, staff_id: int) -> Staff | None:
        return self.db.query(self.model).filter_by(id=staff_id).one_or_none()

    def create(self, data: CreateStaffSchema) -> Staff:
        new_staff = self.model(**data.model_dump())
        self.db.add(new_staff)
        self.db.commit()
        self.db.refresh(new_staff)
        return new_staff

    def update(self, staff_id: int, data: UpdatedStaffSchema) -> Staff | None:
        staff = self.db.query(self.model).filter_by(id=staff_id).one_or_none()
        if not staff:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(staff, key, value)

        self.db.commit()
        self.db.refresh(staff)
        return staff

    def patch(self, staff_id: int, data: PatchStaffSchema) -> Staff | None:
        staff = self.db.query(self.model).filter_by(id=staff_id).one_or_none()
        if not staff:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(staff, key, value)

        self.db.commit()
        self.db.refresh(staff)
        return staff

    def delete(self, staff_id: int) -> Staff | None:
        staff = self.db.query(self.model).filter_by(id=staff_id).one_or_none()
        if not staff:
            return None

        self.db.delete(staff)
        self.db.commit()
        return staff
