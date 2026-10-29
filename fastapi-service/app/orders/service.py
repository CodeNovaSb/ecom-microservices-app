import os
from decimal import Decimal

import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.orders.models import Order
from app.orders.schemas import OrderCreate


def create_order(data: OrderCreate, db: Session) -> Order:
    base_url = os.getenv("DJANGO_BASE_URL", "http://127.0.0.1:8000")

    try:
        with httpx.Client(base_url=base_url, timeout=5.0) as client:
            user_response = client.get(f"/api/v1/users/{data.user_id}/")
            if user_response.status_code == 404:
                raise HTTPException(404, "User not found")
            if not user_response.is_success:
                raise HTTPException(502, "Could not check user in Django")

            product_response = client.get(
                f"/api/v1/products/{data.product_id}/"
            )
            if product_response.status_code == 404:
                raise HTTPException(404, "Product not found")
            if not product_response.is_success:
                raise HTTPException(502, "Could not check product in Django")

            product = product_response.json()

            if product["stock_quantity"] < data.quantity:
                raise HTTPException(409, "Insufficient stock")

            unit_price = Decimal(str(product["price"]))

            new_order = Order(
                user_id=data.user_id,
                product_id=data.product_id,
                quantity=data.quantity,
                unit_price=unit_price,
                total_price=unit_price * data.quantity,
            )

            db.add(new_order)
            db.flush()  # Check the database insert before reducing stock.

            stock_response = client.patch(
                f"/api/v1/products/{data.product_id}/",
                json={
                    "stock_quantity": (
                        product["stock_quantity"] - data.quantity
                    )
                },
            )
            if not stock_response.is_success:
                raise HTTPException(502, "Could not reduce product stock")

            db.commit()
            db.refresh(new_order)
            return new_order

    except httpx.RequestError as exc:
        db.rollback()
        raise HTTPException(502, "Django service is unavailable") from exc
    except Exception:
        db.rollback()
        raise