from django.contrib import admin
from .models import Invention

# Register your models here.


@admin.register(Invention)
class InventionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Invention model.
    """

    list_display = (
        "name",
        "usefulness_level",
        "danger_level",
        "for_students",
        "created_at",
    )
    list_filter = ("danger_level", "for_students")
    search_fields = ("name", "description")
