from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    customer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("customer.id"), nullable=False
    )
    staff_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("staff.id"), nullable=False
    )
    rental_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("rental.id"), nullable=False
    )

    amount: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)

    payment_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    def __repr__(self) -> str:
        return f"Payment(id={self.id}, amount={self.amount}, customer_id={self.customer_id})"
