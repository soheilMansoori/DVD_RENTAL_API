from math import ceil

from sqlalchemy.orm import Session

from .model import Language
from .schema import CreateLanguageSchema


class LanguageService:
    @staticmethod
    def get_all(
        db: Session,
        page: int = 1,
        size: int = 10,
    ):
        total = db.query(Language).count()
        offset = (page - 1) * size
        items = db.query(Language).limit(size).offset(offset).all()

        return {
            "items": items,
            "total": total,
            "page": page,
            "size": size,
            "total_pages": ceil(total / size) if size > 0 else 0,
        }

    @staticmethod
    def create(db: Session, data: CreateLanguageSchema):
        new_language = Language(**data.model_dump())
        db.add(new_language)
        db.commit()
        db.refresh(new_language)
        return new_language

    @staticmethod
    def delete(db: Session, language_id: int):
        language = db.query(Language).filter_by(id=language_id).one_or_none()
        if language:
            db.delete(language)
            db.commit()
            return True
        return False
