from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExcuseViewSet

router = DefaultRouter()
router.register(r"excuses", ExcuseViewSet, basename="excuse")

urlpatterns = [
    path("", include(router.urls)),
]
