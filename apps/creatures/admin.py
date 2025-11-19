from django.contrib import admin
from .models import Creature


@admin.register(Creature)
class CreatureAdmin(admin.ModelAdmin):
    """
    Configuration of how Creature is displayed in the admin panel.
    """

    list_display = ("name", "rarity", "power_level", "favorite_invention", "created_at")
    list_filter = ("rarity", "power_level")
    search_fields = ("name", "description")
