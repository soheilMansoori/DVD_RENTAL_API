from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Category
from .schema import CategoryFiltersSchema, CreateCategorySchema


class CategoryService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Category

    def get_all(
        self, pagination: Pagination, filters: CategoryFiltersSchema
    ) -> PaginatedResponseSchema[Category]:
        query = self.db.query(self.model)

        if filters.name:
            query = query.filter(self.model.name.ilike(f"%{filters.name}%"))

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.limit(pagination.size).offset(offset).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, category_id: int) -> Category | None:
        return self.db.query(self.model).filter_by(id=category_id).one_or_none()

    def create(self, data: CreateCategorySchema) -> Category:
        new_category = self.model(**data.model_dump())
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def delete(self, category_id: int) -> Category | None:
        category = self.db.query(self.model).filter_by(id=category_id).one_or_none()

        if not category:
            return None

        self.db.delete(category)
        self.db.commit()
        return category
