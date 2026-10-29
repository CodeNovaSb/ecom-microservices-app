from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.orders.models import Order
from app.payments.models import Payment, StatusEnum
from app.payments.schemas import PaymentCreate
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/payments", tags=["Payments"])

@router.get("/")
def payments():
    return {"payments page":"working"}


@router.post("/", status_code=201)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    order = db.get(Order, data.order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    existing = db.scalar(
        select(Payment).where(Payment.order_id == data.order_id)
    )
    if existing is not None:
        raise HTTPException(
            status_code=409, detail="Payment already exists for this order"
        )

    payment = Payment(
        order_id=order.id,
        user_id=order.user_id,
        amount=order.total_price,
        status=StatusEnum.pending,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "user_id": payment.user_id,
        "amount": str(payment.amount),
        "status": payment.status.value,
    }


@router.patch("/{payment_id}/pay")
def mark_payment_paid(payment_id: int, db: Session = Depends(get_db)):
    payment = db.get(Payment, payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment.status == StatusEnum.paid:
        raise HTTPException(status_code=409, detail="Payment is already paid")

    order = db.get(Order, payment.order_id)
    order.status = "paid"

    payment.status = StatusEnum.paid
    payment.paid_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(payment)
    return {
        "id": payment.id,
        "order_id": payment.order_id,
        "amount": str(payment.amount),
        "status": payment.status.value,
        "paid_at": payment.paid_at,
    }