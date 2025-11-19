from django.contrib import admin
from .models import Mission


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Mission model.
    """

    list_display = (
        "title",
        "difficulty",
        "xp_reward",
        "is_active",
        "recommended_excuse",
        "required_invention",
        "main_enemy",
        "times_assigned",
        "times_completed",
        "created_at",
    )
    list_filter = ("difficulty", "is_active")
    search_fields = ("title", "description")
