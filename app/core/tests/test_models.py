from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_With_email_successful(self):
        email = "test@example.com"
        password = "test123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,  # password is hashed
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))  # compare hashed password