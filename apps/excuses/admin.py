from django.contrib import admin

# Register your models here.

# optional: you can register the Excuse model to manage it via the admin interface
from .models import Excuse

# admin.site.register(Excuse)


@admin.register(Excuse)
class ExcuseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "power_level", "times_used", "created_at")
    list_filter = ("category", "power_level")
    search_fields = ("title", "description")
