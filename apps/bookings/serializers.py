from rest_framework import serializers
from apps.bookings.models import Booking


class BookingCreateSerializer(serializers.Serializer):
    flight_instance_id = serializers.IntegerField()


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "flight_instance", "status", "created_at"]
