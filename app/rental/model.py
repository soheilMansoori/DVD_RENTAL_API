from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Rental(Base):
    __tablename__ = "rental"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rental_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    return_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    inventory_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("inventory.id"), nullable=False
    )
    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customer.id"), nullable=False
    )
    staff_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("staff.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"Rental(id={self.id}, rental_date={self.rental_date} inventory_id={self.inventory_id} customer_id={self.customer_id} return_date={self.return_date} staff_id={self.staff_id})"
