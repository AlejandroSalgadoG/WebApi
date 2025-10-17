from rest_framework import serializers

from core.models import Summary


def generate_summary(text: str) -> str:
    return text


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ["id", "text", "summary"]
        read_only_fields = ["id", "summary"]

    def create(self, validated_data):
        text = validated_data.get("text", "")
        validated_data["summary"] = generate_summary(text)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        text = validated_data.get("text", instance.text)
        if text != instance.text:
            validated_data["summary"] = generate_summary(text)
        return super().update(instance, validated_data)
