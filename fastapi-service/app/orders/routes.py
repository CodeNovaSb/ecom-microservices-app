from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.orders.models import Order
from app.orders.schemas import OrderResponse, OrderCreate
from app.orders.service import create_order as create_order_service


router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])

@router.get("/", response_model = list[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.scalars(select(Order).order_by(Order.id)).all()

@router.get("/{order_id}", response_model= OrderResponse)
def get_order(order_id: int, db:Session = Depends(get_db)):
    order = db.get(Order, order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=OrderResponse, status_code=201)
def post_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    return create_order_service(order, db)
