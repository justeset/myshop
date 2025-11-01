from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from catalog.models import Category, Product

class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.user.profile.balance = 100.0
        self.user.profile.save()

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Еда", slug="food")
        self.product = Product.objects.create(
            category=self.category, name="Chocolate", slug="chocolate", price=16.0, stock=50
        )

    def test_create_order(self):
        self.client.post("/api/cart/add/", {"product": self.product.id, "quantity": 3}, format="json")
        response = self.client.post("/api/orders/create/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("order_id", response.data)

        response = self.client.get("/api/cart/")
        self.assertEqual(len(response.data["items"]), 0)

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 47)

    def test_order_insufficient_balance(self):
        self.user.profile.balance = 10
        self.user.profile.save()

        self.client.post("/api/cart/add/", {"product": self.product.id, "quantity": 3}, format="json")
        response = self.client.post("/api/orders/create/")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)
