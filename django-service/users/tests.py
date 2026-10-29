from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Users


class UserApiTests(APITestCase):
    def test_user_list_and_detail_endpoints(self):
        user = Users.objects.create(
            name="Test user",
            mail="test@example.com",
            address="Test address",
            phone_no="555-0100",
        )

        list_response = self.client.get("/api/v1/users/")
        detail_response = self.client.get(f"/api/v1/users/{user.id}/")

        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_response.data["mail"], "test@example.com")
