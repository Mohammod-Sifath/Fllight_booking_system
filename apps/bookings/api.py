from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.bookings.serializers import BookingCreateSerializer, BookingSerializer
from apps.bookings.services import create_booking, BookingError
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from apps.bookings.models import Booking
from apps.bookings.serializers import BookingSerializer
from apps.bookings.services import cancel_booking


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def booking_create(request):
    serializer = BookingCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    flight_instance_id = serializer.validated_data["flight_instance_id"]

    try:
        booking = create_booking(user=request.user, flight_instance_id=flight_instance_id)
    except BookingError as e:
        # full / business-rule failure => conflict
        return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

    return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)

@api_view(["PATCH", "POST"])
@permission_classes([IsAuthenticated])
def booking_cancel(request, booking_id: int):
    booking = get_object_or_404(Booking, id=booking_id)

    try:
        booking = cancel_booking(booking=booking, user=request.user)
    except PermissionDenied as e:
        return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)

    return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)