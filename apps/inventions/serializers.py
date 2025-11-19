from rest_framework import serializers
from .models import Invention


class InventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invention
        fields = [
            "id",
            "name",
            "description",
            "usefulness_level",
            "danger_level",
            "for_students",
            "created_at",
            "updated_at",
            "student_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
