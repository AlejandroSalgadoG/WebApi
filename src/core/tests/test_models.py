from django.test import TestCase
from django.contrib.auth import get_user_model


def get_payload():
    return {
        "username": "test",
        "password": "test123",
    }


class ModelTests(TestCase):
    def test_create_user_successful(self):
        payload = get_payload()

        user = get_user_model().objects.create_user(**payload)

        self.assertEqual(user.username, payload["username"])
        self.assertTrue(user.check_password(payload["password"]))

    def test_new_user_wo_username_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_new_user_wo_password_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("test", "")

    def test_create_superuser(self):
        payload = get_payload()
        user = get_user_model().objects.create_superuser(**payload)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
