from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class FilmCategory(Base):
    __tablename__ = "film_category"

    film_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("film.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("category.id"), primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"FilmCategory(film_id={self.film_id}, category_id={self.category_id})"
