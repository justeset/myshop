from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from catalog.models import Category, Product

class CartTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.user.profile.balance = 100.0
        self.user.profile.save()

        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Сладости", slug="sladosti")
        self.product = Product.objects.create(
            category=self.category,
            name="Chocolate",
            slug="chocolate",
            price=16.0,
            stock=50
        )

    def test_add_to_cart(self):
        response = self.client.post("/api/cart/add/", {"product": self.product.id, "quantity": 3}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["quantity"], 3)

    def test_add_same_product_twice(self):
        self.client.post("/api/cart/add/", {"product": self.product.id, "quantity": 2}, format="json")
        response = self.client.post("/api/cart/add/", {"product": self.product.id, "quantity": 3}, format="json")
        self.assertEqual(response.data["quantity"], 5)
