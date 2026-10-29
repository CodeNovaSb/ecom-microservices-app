from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Product


class ProductApiTests(APITestCase):
    def test_product_list_and_detail_endpoints(self):
        product = Product.objects.create(
            name="Test product",
            description="A product for API tests",
            price="12.50",
            product_image="https://example.com/product.png",
            alt_text="Test product",
            stock_quantity=4,
        )

        list_response = self.client.get("/api/v1/products/")
        detail_response = self.client.get(f"/api/v1/products/{product.id}/")

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data["stock_quantity"], 4)

    def test_product_patch_updates_stock(self):
        product = Product.objects.create(
            name="Test product",
            description="A product for API tests",
            price="12.50",
            product_image="https://example.com/product.png",
            alt_text="Test product",
            stock_quantity=4,
        )

        response = self.client.patch(
            f"/api/v1/products/{product.id}/",
            {"stock_quantity": 2},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["stock_quantity"], 2)
