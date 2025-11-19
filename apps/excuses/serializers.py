from rest_framework import serializers
from .models import Excuse


class ExcuseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Excuse model.
    Traslates Excuse model instances into JSON format and vice versa.
    """

    class Meta:
        model = Excuse
        fields = "__all__"

    read_only_fields = ("id", "created_at", "updated_at")
