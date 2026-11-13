from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Address
from .schema import (
    AddressFilters,
    CreateAddressSchema,
    PatchAddressSchema,
    UpdateAddressSchema,
)


class AddressService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Address

    def get_all(
        self, pagination: Pagination, filters: AddressFilters
    ) -> PaginatedResponseSchema[Address]:
        query = self.db.query(self.model)

        if filters.address:
            query = query.filter(self.model.address.ilike(f"%{filters.address}%"))

        if filters.address2:
            query = query.filter(self.model.address2.ilike(f"%{filters.address2}%"))

        if filters.district:
            query = query.filter(self.model.district.ilike(f"%{filters.district}%"))

        if filters.phone:
            query = query.filter(self.model.phone.ilike(f"%{filters.phone}%"))

        if filters.city_id:
            query = query.filter_by(city_id=filters.city_id)

        if filters.postal_code:
            query = query.filter_by(postal_code=filters.postal_code)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.offset(offset).limit(pagination.size).all()

        return PaginatedResponseSchema(
            items=items, page=pagination.page, size=pagination.size, total=total
        )

    def get_by_id(self, address_id: int) -> Address | None:
        return self.db.query(self.model).filter_by(id=address_id).one_or_none()

    def create(self, data: CreateAddressSchema) -> Address:
        new_address = self.model(**data.model_dump())
        self.db.add(new_address)
        self.db.commit()
        self.db.refresh(new_address)
        return new_address

    def update(self, address_id: int, data: UpdateAddressSchema) -> Address | None:
        address = self.db.query(self.model).filter_by(id=address_id).one_or_none()
        if not address:
            return None

        update_data = data.model_dump()
        for key, value in update_data.items():
            setattr(address, key, value)

        self.db.commit()
        self.db.refresh(address)

        return address

    def patch(self, address_id: int, data: PatchAddressSchema) -> Address | None:
        address = self.db.query(self.model).filter_by(id=address_id).one_or_none()
        if not address:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(address, key, value)

        self.db.commit()
        self.db.refresh(address)

        return address

    def delete(self, address_id: int) -> Address | None:
        address = self.db.query(self.model).filter_by(id=address_id).one_or_none()

        if not address:
            return None

        self.db.delete(address)
        self.db.commit()
        return address
