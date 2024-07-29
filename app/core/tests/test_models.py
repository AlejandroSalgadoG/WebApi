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

    def test_new_user_email_normalized(self):
        sample_emails =[
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@EXAMPLE.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_wo_email_raise_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")