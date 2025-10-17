from rest_framework import serializers

from core.models import Summary


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ["id", "text", "summary"]
        read_only_fields = ["id"]
