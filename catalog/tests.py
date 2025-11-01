from django.test import TestCase
from rest_framework.test import APIClient
from users.models import UserProfile
from catalog.models import Category, Product
from django.contrib.auth.models import User

class ProductTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_superuser(username="admin", password="adminpass")
        self.client.force_authenticate(user=self.admin)
        self.category = Category.objects.create(name="Еда", slug="food")

    def test_create_product(self):
        data = {
            "category": self.category.id,
            "name": "Chocolate",
            "slug": "chocolate",
            "price": "16.00",
            "stock": 50,
            "available": True
        }
        response = self.client.post("/api/catalog/products/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "Chocolate")

    def test_list_products(self):
        Product.objects.create(category=self.category, name="Еда", slug="food", price=10.0, stock=10)
        response = self.client.get("/api/catalog/products/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
