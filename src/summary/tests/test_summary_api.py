from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Summary
from summary.serializers import SummarySerializer


SUMMARY_LIST_URL = reverse("summary:summary-list")

def detail_url(summary_id):
    return reverse("summary:summary-detail", args=[summary_id])


def create_summary(user, **kwargs):
    attrs = {
        "text": "Complete text",
        "summary": "Summary",
    }
    attrs.update(kwargs)
    return Summary.objects.create(user=user, **attrs)


class PublicSummaryApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SUMMARY_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateSummaryApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        payload = {
            "username": "test",
            "password": "test123",
        }

        self.user = get_user_model().objects.create_user(**payload)

        self.client.force_authenticate(self.user)

    def test_retrieve_summaries(self):
        create_summary(user=self.user)
        create_summary(user=self.user)

        res = self.client.get(SUMMARY_LIST_URL)

        summaries = Summary.objects.all().order_by("-id")
        serializer = SummarySerializer(summaries, many=True)

        self.assertEqual(res.data, serializer.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_summary_limited_to_user(self):
        payload = {
            "username": "other",
            "password": "test123",
        }

        other_user = get_user_model().objects.create_user(**payload)

        create_summary(user=other_user)
        create_summary(user=self.user)

        res = self.client.get(SUMMARY_LIST_URL)

        summaries = Summary.objects.filter(user=self.user).order_by("-id")
        serializer = SummarySerializer(summaries, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_summary(self):
        payload = {
            "text": "Example text.",
        }
        res = self.client.post(SUMMARY_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        summary = Summary.objects.get(id=res.data["id"])

        self.assertEqual(summary.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(summary, k), v)

    def test_create_auto_generated_summary(self):
        payload = {
            "text": "Example text.",
        }

        res = self.client.post(SUMMARY_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertIn("summary", res.data)
        self.assertNotEqual(res.data["summary"], "")
        self.assertEqual(res.data["text"], payload["text"])

        # Verify in database
        summary = Summary.objects.get(id=res.data["id"])
        self.assertEqual(summary.text, payload["text"])
        self.assertNotEqual(summary.summary, "")
        self.assertEqual(summary.user, self.user)

    def test_create_summary_ignores_provided_summary(self):
        """Test that provided summary is ignored and auto-generated instead."""
        payload = {
            "text": "This is the actual text.",
            "summary": "This should be ignored.",
        }

        res = self.client.post(SUMMARY_LIST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.data["summary"], payload["summary"])

    def test_update_summary_regenerates_summary(self):
        summary = create_summary(user=self.user, text="Original text.", summary="Original summary.")

        payload = {
            "text": "Updated text that is different.",
        }

        url = detail_url(summary.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        summary.refresh_from_db()
        self.assertEqual(summary.text, payload["text"])
        self.assertNotEqual(summary.summary, "Original summary.")
