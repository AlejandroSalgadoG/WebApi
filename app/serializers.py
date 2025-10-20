from rest_framework import serializers

from app.models import Info, Task


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'
        read_only_fields = ['id', 'user']


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError("start_date cannot be after end_date")
        return attrs


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_type', 'status', 'created_at', 'updated_at', 'result', 'error_message']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'result', 'error_message']
