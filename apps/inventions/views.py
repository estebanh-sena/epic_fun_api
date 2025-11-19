from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
import random

from .models import Invention
from .serializers import InventionSerializer

# Create your views here.


class InventionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing invention instances.
    """

    queryset = Invention.objects.all().order_by("-created_at")
    serializer_class = InventionSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], url_path="random")
    def random_invention(self, request):
        """
        Retrieve a random invention.
        """
        queryset = self.get_queryset()
        count = queryset.count()

        if count == 0:
            return Response(
                {"detail": "No inventions available."}, status=status.HTTP_404_NOT_FOUND
            )

        random_index = random.randint(0, count - 1)
        invention = queryset[random_index]
        serializer = self.get_serializer(invention)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="safe")
    def safe_inventions(self, request):
        """
        Retrieve all inventions marked as safe.
        """
        queryset = self.get_queryset().filter(danger_level__lte=2)

        if not queryset.exists():
            return Response(
                {"detail": "No safe inventions available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="for-students")
    def for_students_inventions(self, request):
        """
        Retrieve inventions suitable for students (danger_level 1).
        """
        queryset = self.get_queryset().filter(for_students=True)

        if not queryset.exists():
            return Response(
                {"detail": "No inventions suitable for students available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
