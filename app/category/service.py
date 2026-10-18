from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db

from .model import Category
from .schema import CreateCategorySchema


class CategoryService:
    db: Session
    model: type[Category] = Category

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_all(self, pagination: Pagination):
        page, size, q = (pagination.page, pagination.size, pagination.q)
        db, model = self.db, self.model

        query = db.query(model)

        if not q is None:
            query = query.filter(model.city.ilike(f"%{q}%"))

        total = query.count()
        offset = (page - 1) * size
        items = query.limit(size).offset(offset).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    def get_by_id(self, category_id: int):
        return self.db.query(self.model).filter_by(id=category_id).one_or_none()

    def create(self, data: CreateCategorySchema):
        db, model = self.db, self.model
        new_category = model(**data.model_dump())
        db.add(new_category)
        db.commit()
        db.refresh(new_category)
        return new_category

    def delete(self, category_id: int):
        db, model = self.db, self.model
        category = db.query(model).filter_by(id=category_id).one_or_none()
        if category:
            db.delete(category)
            db.commit()
            return True
        return False
