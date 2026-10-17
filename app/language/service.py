from math import ceil
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import Pagination, get_db

from .model import Language
from .schema import CreateLanguageSchema


class LanguageService:
    db: Session
    model: type[Language] = Language

    def __init__(self, db: Annotated[Session, Depends(get_db)]) -> None:
        self.db = db

    def get_all(self, pagination: Pagination):
        page, size, q = (pagination.page, pagination.size, pagination.q)
        db, model = self.db, self.model

        query = db.query(model)

        if not q is None:
            query = query.filter(model.name.ilike(f"%{q}%"))

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

    def get_by_id(self, language_id: int):
        return self.db.query(self.model).filter_by(id=language_id).one_or_none()

    def create(self, data: CreateLanguageSchema):
        db, model = self.db, self.model
        new_language = model(**data.model_dump())
        db.add(new_language)
        db.commit()
        db.refresh(new_language)
        return new_language

    def delete(self, language_id: int):
        db, model = self.db, self.model
        language = db.query(model).filter_by(id=language_id).one_or_none()
        if language:
            db.delete(language)
            db.commit()
            return True
        return False
