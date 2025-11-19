from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
import random

from .models import Mission
from .serializers import MissionSerializer


class MissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Mission.
    Provides:
    - Standard CRUD operations
    - Custom actions: random_active, for_beginners, by_creature, assign, complete
    """

    queryset = (
        Mission.objects.select_related(
            "recommended_excuse",
            "required_invention",
            "main_enemy",
        )
        .all()
        .order_by("-created_at")
    )

    serializer_class = MissionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], url_path="random-active")
    def random_active(self, request):
        """
        Returns a random active mission.
        URL: /api/missions/random-active/
        """
        queryset = self.get_queryset().filter(is_active=True)
        count = queryset.count()

        if count == 0:
            return Response(
                {"detail": "No active missions available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        random_index = random.randint(0, count - 1)
        mission = queryset[random_index]

        # Optional: increment assignment counter
        Mission.objects.filter(pk=mission.pk).update(
            times_assigned=F("times_assigned") + 1
        )
        mission.refresh_from_db(fields=["times_assigned"])

        serializer = self.get_serializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="for-beginners")
    def for_beginners(self, request):
        """
        Returns missions with 'easy' difficulty.
        URL: /api/missions/for-beginners/
        """
        queryset = self.get_queryset().filter(difficulty=Mission.Difficulty.EASY)

        if not queryset.exists():
            return Response(
                {"detail": "No beginner missions found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="by-creature")
    def by_creature(self, request):
        """
        Filters missions by main_enemy (creature id).
        Query param:
        - creature_id (required)
        Example:
        /api/missions/by-creature/?creature_id=1
        """
        creature_id = request.query_params.get("creature_id")

        if not creature_id:
            return Response(
                {"detail": "You must provide a 'creature_id' query parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(main_enemy_id=creature_id)

        if not queryset.exists():
            return Response(
                {"detail": "No missions found for this creature."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="assign")
    def assign(self, request, pk=None):
        """
        Marks a specific mission as assigned.
        URL: /api/missions/{id}/assign/
        """
        mission = self.get_object()
        Mission.objects.filter(pk=mission.pk).update(
            times_assigned=F("times_assigned") + 1
        )
        mission.refresh_from_db(fields=["times_assigned"])

        serializer = self.get_serializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        """
        Marks a specific mission as completed.
        URL: /api/missions/{id}/complete/
        """
        mission = self.get_object()
        Mission.objects.filter(pk=mission.pk).update(
            times_completed=F("times_completed") + 1
        )
        mission.refresh_from_db(fields=["times_completed"])

        serializer = self.get_serializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)
