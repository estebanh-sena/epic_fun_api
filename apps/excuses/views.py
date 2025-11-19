from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Excuse
from .serializers import ExcuseSerializer

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
import random


class ExcuseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing excuse instances.
    """

    queryset = Excuse.objects.all().order_by("-created_at")
    serializer_class = ExcuseSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], url_path="random")
    def random_excuse(self, request):
        """
        Retrieve a random excuse.
        """
        queryset = self.get_queryset()
        count = queryset.count()

        if count == 0:
            return Response(
                {"detail": "No excuses available."},
                status=status.HTTP_404_NOT_FOUND,
            )

        random_index = random.randint(0, count - 1)
        excuse = queryset[random_index]

        excuse.times_used += 1
        excuse.save(update_fields=["times_used"])

        serializer = self.get_serializer(excuse)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # detail=False indicates this action applies to the collection, not a single instance
    # and the URL not includes a pk
    @action(detail=False, methods=["get"], url_path="top")
    def top_excuses(self, request):
        """
        Retrieve the top excuses based on times used.
        """

        by = request.query_params.get("by", "power")
        limit_param = request.query_params.get("limit", "5")

        try:
            limit = int(limit_param)
        except ValueError:
            limit = 5

        if by == "usage":
            queryset = self.get_queryset().order_by("-times_used")
        else:
            queryset = self.get_queryset().order_by("-power_level")

        top_excuses = queryset[:limit]
        serializer = self.get_serializer(top_excuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="by-category")
    def by_category(self, request):
        """
        Retrieve excuses filtered by category.
        """
        category = request.query_params.get("category")
        if not category:
            return Response(
                {"detail": "Category parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(category=category)

        if not queryset.exists():
            return Response(
                {"detail": f"No excuses found for category '{category}'."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
