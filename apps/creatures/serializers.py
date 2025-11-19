from rest_framework import serializers
from .models import Creature


class CreatureSerializer(serializers.ModelSerializer):
    """
    Serializer for the Creature model.
    Translates between Creature objects and JSON.
    """

    class Meta:
        model = Creature
        fields = [
            "id",
            "name",
            "description",
            "power_level",
            "rarity",
            "favorite_invention",
            "created_at",
            "updated_at",
            "student_name",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
