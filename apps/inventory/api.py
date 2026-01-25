from django.db.models import Count, F, Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.bookings.models import Booking
from apps.inventory.models import FlightInstance
from apps.inventory.serializers import FlightInstanceAvailabilitySerializer


@api_view(["GET"])
def availability_list(request):
    qs = (
        FlightInstance.objects.select_related("flight")
        .annotate(
            booked_active=Count(
                "bookings",
                filter=Q(bookings__status__in=["pending", "confirmed"]),
            )
        )
        .annotate(seats_left=F("capacity") - F("booked_active"))
        .order_by("departure_at")
    )

    serializer = FlightInstanceAvailabilitySerializer(qs, many=True)
    return Response(serializer.data)
