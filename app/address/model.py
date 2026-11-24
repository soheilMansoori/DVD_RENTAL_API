from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.city.model import City


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(String(50), nullable=False)
    address2: Mapped[str | None] = mapped_column(String(50), nullable=True)
    district: Mapped[str] = mapped_column(String(20), nullable=False)
    postal_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)

    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("city.id"), nullable=False)

    city: Mapped[City] = relationship(back_populates="addresses")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"""Address(id={self.id}, address={self.address!r}, address2={self.address2!r}, district={self.district}, postal_code={self.postal_code}, phone={self.phone}, city_id={self.city_id})"""
