from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from app.core.dependencies import Pagination, get_db

from .model import Address
from .schema import CreateAddressSchema, PatchAddressSchema, UpdateAddressSchema


class AddressService:
    db: Session
    model: type[Address] = Address

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_all(self, pagination: Pagination):
        page, size, q = (pagination.page, pagination.size, pagination.q)
        model = self.model
        query = self.db.query(model)

        if not q is None:
            query = query.filter(
                or_(
                    model.address.ilike(f"%{q}%"),
                    model.address2.ilike(f"%{q}%"),
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

    def get_by_id(self, address_id: int):
        return self.db.query(self.model).filter_by(id=address_id).one_or_none()

    def create(self, data: CreateAddressSchema):
        db, model = (self.db, self.model)

        new_actor = model(**data.model_dump())
        db.add(new_actor)
        db.commit()
        db.refresh(new_actor)

        return new_actor

    def update(self, address_id: int, data: UpdateAddressSchema):
        db, model = (self.db, self.model)
        address = db.query(model).filter_by(id=address_id).one_or_none()
        if not address:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(address, key, value)

        db.commit()
        db.refresh(address)
        return address

    def patch(self, address_id: int, data: PatchAddressSchema):
        db, model = (self.db, self.model)
        address = db.query(model).filter_by(id=address_id).one_or_none()
        if not address:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(address, key, value)

        db.commit()
        db.refresh(address)
        return address

    def delete(self, address_id: int):
        db, model = (self.db, self.model)
        address = db.query(model).filter_by(id=address_id).one_or_none()
        if address:
            db.delete(address)
            db.commit()
            return True

        return False
