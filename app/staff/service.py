from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from app.core.dependencies import Pagination, get_db

from .model import Staff
from .schema import (
    CreateStaffSchema,
    PatchStaffSchema,
    UpdatedStaffSchema,
)


class StaffService:
    db: Session
    model: type[Staff] = Staff

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
                    model.username.ilike(f"%{q}%"),
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

    def get_by_id(self, staff_id: int):
        return self.db.query(self.model).filter_by(id=staff_id).one_or_none()

    def create(self, data: CreateStaffSchema):
        db, model = (self.db, self.model)

        new_staff = model(**data.model_dump())
        db.add(new_staff)
        db.commit()
        db.refresh(new_staff)

        return new_staff

    def update(self, staff_id: int, data: UpdatedStaffSchema):
        db, model = (self.db, self.model)
        staff = db.query(model).filter_by(id=staff_id).one_or_none()
        if not staff:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(staff, key, value)

        db.commit()
        db.refresh(staff)
        return staff

    def patch(self, staff_id: int, data: PatchStaffSchema):
        db, model = (self.db, self.model)
        staff = db.query(model).filter_by(id=staff_id).one_or_none()
        if not staff:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(staff, key, value)

        db.commit()
        db.refresh(staff)
        return staff

    def delete(self, staff_id: int):
        db, model = (self.db, self.model)
        staff = db.query(model).filter_by(id=staff_id).one_or_none()
        if staff:
            db.delete(staff)
            db.commit()
            return True

        return False
