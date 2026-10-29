from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import mapped_column

from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = mapped_column(Integer, primary_key=True, index=True)
    user_id = mapped_column(Integer, nullable=False)
    product_id = mapped_column(Integer, nullable=False)
    quantity = mapped_column(Integer, nullable=False)
    unit_price = mapped_column(Numeric(10, 2), nullable=False)
    total_price = mapped_column(Numeric(10, 2), nullable=False)
    status = mapped_column(String(20), nullable=False, default="pending")
    created_at = mapped_column(DateTime, server_default=func.current_timestamp(), nullable=False)
    __table_args__=(
        CheckConstraint("Quantity > 0"),
        CheckConstraint("unit_price >= 0"),
        CheckConstraint("total_price >=0"),
    )


# id,
# user_id,
# product_id,
# quantity, unit_price, total_price, status, and created_at