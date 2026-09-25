from django.contrib import admin

from .models import DailyEntry, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "diet_preference", "weight_kg", "started_on")
    list_filter = ("diet_preference",)


@admin.register(DailyEntry)
class DailyEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "walked_km", "strength_done", "mobility_done", "points")
    list_filter = ("user", "date", "strength_done")
    date_hierarchy = "date"
