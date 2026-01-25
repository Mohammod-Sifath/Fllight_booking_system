from rest_framework import serializers
from apps.inventory.models import FlightInstance


class FlightInstanceAvailabilitySerializer(serializers.ModelSerializer):
    booked_active = serializers.IntegerField(read_only=True)
    seats_left = serializers.IntegerField(read_only=True)

    class Meta:
        model = FlightInstance
        fields = [
            "id",
            "flight",
            "departure_at",
            "capacity",
            "booked_active",
            "seats_left",
        ]
