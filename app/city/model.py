from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.address.model import Address
    from app.country.model import Country


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(50), nullable=False)

    country_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("country.id"), nullable=False
    )

    country: Mapped[Country] = relationship(back_populates="cities")
    addresses: Mapped[list[Address]] = relationship(back_populates="city")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"City(id={self.id}, city={self.city!r}, country_id={self.country_id})"
