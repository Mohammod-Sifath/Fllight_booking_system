from django.contrib import admin
from .models import Flight, FlightInstance


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("code", "origin", "destination", "is_active")
    list_filter = ("is_active",)
    search_fields = ("code", "origin", "destination")


@admin.register(FlightInstance)
class FlightInstanceAdmin(admin.ModelAdmin):
    list_display = ("flight", "departure_at", "arrival_at", "capacity", "is_active")
    list_filter = ("is_active", "departure_at")
