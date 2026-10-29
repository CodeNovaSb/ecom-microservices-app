import os
import tempfile
import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

TEST_DB_DIR = tempfile.TemporaryDirectory()
os.environ["DATABASE_URL"] = f"sqlite:///{TEST_DB_DIR.name}/test.db"

from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from main import app
from app.orders.models import Order
from app.orders.service import create_order
from app.orders.schemas import OrderCreate
from app.payments.models import Payment


class FastApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        engine.dispose()
        TEST_DB_DIR.cleanup()

    def setUp(self):
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def _django_response(self, status_code, payload=None):
        response = MagicMock()
        response.status_code = status_code
        response.is_success = 200 <= status_code < 300
        if payload is not None:
            response.json.return_value = payload
        return response

    def test_order_creation_reduces_stock(self):
        user_response = self._django_response(200, {"id": 1})
        product_response = self._django_response(
            200, {"price": "12.50", "stock_quantity": 4}
        )
        stock_response = self._django_response(200)
        http_client = MagicMock()
        http_client.__enter__.return_value = http_client
        http_client.get.side_effect = [user_response, product_response]
        http_client.patch.return_value = stock_response

        with patch("app.orders.service.httpx.Client", return_value=http_client):
            with SessionLocal() as db:
                order = create_order(
                    OrderCreate(user_id=1, product_id=1, quantity=2), db
                )

        self.assertEqual(order.total_price, Decimal("25.00"))
        http_client.patch.assert_called_once_with(
            "/api/v1/products/1/",
            json={"stock_quantity": 2},
        )

    def test_order_rejects_insufficient_stock(self):
        http_client = MagicMock()
        http_client.__enter__.return_value = http_client
        http_client.get.side_effect = [
            self._django_response(200, {"id": 1}),
            self._django_response(
                200, {"price": "12.50", "stock_quantity": 1}
            ),
        ]

        with patch("app.orders.service.httpx.Client", return_value=http_client):
            with SessionLocal():
                response = self.client.post(
                    "/api/v1/orders/",
                    json={"user_id": 1, "product_id": 1, "quantity": 2},
                )

        self.assertEqual(response.status_code, 409)
        http_client.patch.assert_not_called()

    def test_order_rejects_unknown_user(self):
        http_client = MagicMock()
        http_client.__enter__.return_value = http_client
        http_client.get.return_value = self._django_response(404)

        with patch("app.orders.service.httpx.Client", return_value=http_client):
            response = self.client.post(
                "/api/v1/orders/",
                json={"user_id": 99, "product_id": 1, "quantity": 1},
            )

        self.assertEqual(response.status_code, 404)

    def test_order_rejects_unknown_product(self):
        http_client = MagicMock()
        http_client.__enter__.return_value = http_client
        http_client.get.side_effect = [
            self._django_response(200, {"id": 1}),
            self._django_response(404),
        ]

        with patch("app.orders.service.httpx.Client", return_value=http_client):
            response = self.client.post(
                "/api/v1/orders/",
                json={"user_id": 1, "product_id": 99, "quantity": 1},
            )

        self.assertEqual(response.status_code, 404)

    def _create_order(self):
        with SessionLocal() as db:
            order = Order(
                user_id=1,
                product_id=1,
                quantity=1,
                unit_price=Decimal("12.50"),
                total_price=Decimal("12.50"),
            )
            db.add(order)
            db.commit()
            db.refresh(order)
            return order.id

    def test_payment_creation_and_duplicate_rejection(self):
        order_id = self._create_order()

        response = self.client.post(
            "/api/v1/payments/", json={"order_id": order_id}
        )
        duplicate_response = self.client.post(
            "/api/v1/payments/", json={"order_id": order_id}
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["status"], "pending")
        self.assertEqual(duplicate_response.status_code, 409)

    def test_payment_cannot_be_marked_paid_twice(self):
        order_id = self._create_order()
        payment_response = self.client.post(
            "/api/v1/payments/", json={"order_id": order_id}
        )
        payment_id = payment_response.json()["id"]

        paid_response = self.client.patch(
            f"/api/v1/payments/{payment_id}/pay"
        )
        second_paid_response = self.client.patch(
            f"/api/v1/payments/{payment_id}/pay"
        )

        self.assertEqual(paid_response.status_code, 200)
        self.assertEqual(paid_response.json()["status"], "paid")
        self.assertEqual(second_paid_response.status_code, 409)

        with SessionLocal() as db:
            payment = db.get(Payment, payment_id)
            self.assertEqual(payment.status.value, "paid")


if __name__ == "__main__":
    unittest.main()
