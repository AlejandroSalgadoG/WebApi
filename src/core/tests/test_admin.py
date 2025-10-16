from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from rest_framework import status


class AdminSiteTests(TestCase):
    def setUp(self):  # method called before executing tests
        self.client = Client()  # django http client

        admin_payload = {"username": "admin", "password": "test123"}
        user_payload = {"username": "user", "password": "test123"}

        self.admin_user = get_user_model().objects.create_superuser(**admin_payload)
        self.user = get_user_model().objects.create_user(**user_payload)

        self.client.force_login(self.admin_user)

    def test_users_list(self):
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.username)

    def test_edit_user_page(self):
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_user_page(self):
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
