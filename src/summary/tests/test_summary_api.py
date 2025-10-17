from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Summary
from summary.serializers import SummarySerializer


SUMMARY_URL = reverse("summary:summary-list")


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
        res = self.client.get(SUMMARY_URL)
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

        res = self.client.get(SUMMARY_URL)

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

        res = self.client.get(SUMMARY_URL)

        summaries = Summary.objects.filter(user=self.user).order_by("-id")
        serializer = SummarySerializer(summaries, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_summary(self):
        payload = {
            "text": "Example text.",
            "summary": "Example summary.",
        }
        res = self.client.post(SUMMARY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        summary = Summary.objects.get(id=res.data["id"])

        self.assertEqual(summary.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(summary, k), v)
