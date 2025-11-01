from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.user.profile.balance = 100.0
        self.user.profile.save()
        self.client.force_authenticate(user=self.user)

    def test_login_user(self):
        data = {"username": "testuser", "password": "pass123"}
        response = self.client.post("/api/token/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
