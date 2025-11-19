from rest_framework import serializers
from .models import Mission


class MissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Mission model.
    Translates Mission instances to/from JSON representation.
    """

    class Meta:
        model = Mission
        fields = [
            "id",
            "title",
            "description",
            "difficulty",
            "xp_reward",
            "is_active",
            "recommended_excuse",
            "required_invention",
            "main_enemy",
            "times_assigned",
            "times_completed",
            "created_at",
            "updated_at",
            "student_name",
        ]
        read_only_fields = [
            "id",
            "times_assigned",
            "times_completed",
            "created_at",
            "updated_at",
        ]
