from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db
from app.core.schemas import PaginatedResponseSchema

from .model import Language
from .schema import CreateLanguageSchema


class LanguageService:
    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db: Session = db
        self.model = Language

    def get_all(self, pagination: Pagination) -> PaginatedResponseSchema[Language]:
        query = self.db.query(self.model)

        total = query.count()
        offset = (pagination.page - 1) * pagination.size
        items = query.limit(pagination.size).offset(offset).all()

        return PaginatedResponseSchema(
            items=items,
            total=total,
            page=pagination.page,
            size=pagination.size,
        )

    def get_by_id(self, language_id: int) -> Language | None:
        return self.db.query(self.model).filter_by(id=language_id).one_or_none()

    def create(self, data: CreateLanguageSchema) -> Language:
        new_language = self.model(**data.model_dump())
        self.db.add(new_language)
        self.db.commit()
        self.db.refresh(new_language)
        return new_language

    def delete(self, language_id: int) -> Language | None:
        language = self.db.query(self.model).filter_by(id=language_id).one_or_none()
        if not language:
            return None

        self.db.delete(language)
        self.db.commit()
        return language
