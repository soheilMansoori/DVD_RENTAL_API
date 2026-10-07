from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Film(Base):
    __tablename__ = "film"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    release_year: Mapped[int] = mapped_column(Integer, nullable=True)
    language_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("language.id"), nullable=False
    )
    rental_duration: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    rental_rate: Mapped[float] = mapped_column(
        Numeric(4, 2), default=0.0, nullable=False
    )
    length: Mapped[int] = mapped_column(Integer, nullable=True)
    replacement_cost: Mapped[float] = mapped_column(
        Numeric(5, 2), default=0.0, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
