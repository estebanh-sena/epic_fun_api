from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
import random

from .models import Creature
from .serializers import CreatureSerializer


class CreatureViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Creature.
    Includes:
    - Standard CRUD (list, retrieve, create, update, destroy)
    - Custom actions: random, legendary, by_power_range
    """

    queryset = (
        Creature.objects.select_related("favorite_invention")
        .all()
        .order_by("-created_at")
    )
    serializer_class = CreatureSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], url_path="random")
    def random_creature(self, request):
        """
        Returns a random creature.
        URL: /api/creatures/random/
        """
        queryset = self.get_queryset()
        count = queryset.count()

        if count == 0:
            return Response(
                {"detail": "No creatures available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        random_index = random.randint(0, count - 1)
        creature = queryset[random_index]

        serializer = self.get_serializer(creature)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="legendary")
    def legendary_creatures(self, request):
        """
        Returns creatures with rarity 'legendary'.
        URL: /api/creatures/legendary/
        """
        queryset = self.get_queryset().filter(rarity=Creature.Rarity.LEGENDARY)

        if not queryset.exists():
            return Response(
                {"detail": "No legendary creatures found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="by-power-range")
    def by_power_range(self, request):
        """
        Filters creatures by power level range.
        Query params:
        - min_power (optional, default 1)
        - max_power (optional, default 10)

        Examples:
        /api/creatures/by-power-range/?min_power=5
        /api/creatures/by-power-range/?min_power=3&max_power=7
        """
        min_power_param = request.query_params.get("min_power", "1")
        max_power_param = request.query_params.get("max_power", "10")

        try:
            min_power = int(min_power_param)
            max_power = int(max_power_param)
        except ValueError:
            return Response(
                {"detail": "min_power and max_power must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(
            power_level__gte=min_power,
            power_level__lte=max_power,
        )

        if not queryset.exists():
            return Response(
                {"detail": "No creatures found in this power range."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
