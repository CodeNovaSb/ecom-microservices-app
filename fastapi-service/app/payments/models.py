
from app.database import Base
from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum, CheckConstraint, ForeignKey, DateTime, func, Numeric, String, Integer
from sqlalchemy.orm import mapped_column


class StatusEnum(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (CheckConstraint("amount >= 0",
                                      name="payments_amount_nonnegative", ),
                      )

    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, nullable=False)
    order_id = mapped_column(ForeignKey("orders.id", ondelete="RESTRICT"),
                             nullable=False,
                             unique=True)
    description = mapped_column(String(255), nullable=True)
    amount = mapped_column(Numeric(12, 2), nullable=False)
    status = mapped_column(
        SQLAlchemyEnum(StatusEnum,
                       name="status_enum",
                       create_constraint=True, ),
        nullable=False,
        default=StatusEnum.pending, )

    created_at = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
    paid_at = mapped_column(DateTime, nullable=True)
