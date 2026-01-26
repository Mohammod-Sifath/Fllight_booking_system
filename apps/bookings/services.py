from django.db import transaction
from django.db.models import Count

from apps.bookings.models import Booking
from apps.inventory.models import FlightInstance

from django.core.exceptions import PermissionDenied
from django.db import transaction



class BookingError(Exception):
    pass


@transaction.atomic
def create_booking(*, user, flight_instance_id: int) -> Booking:
    """
    Create a booking for a user on a flight instance.

    Rules:
    - A flight instance cannot be overbooked.
    - If capacity is full, raise BookingError.
    """

    flight_instance = (
        FlightInstance.objects
        .select_for_update()
        .get(id=flight_instance_id, is_active=True)
    )

    active_bookings_count = (
        Booking.objects
        .filter(
            flight_instance=flight_instance,
            status__in=[
                Booking.STATUS_PENDING,
                Booking.STATUS_CONFIRMED,
            ],
        )
        .count()
    )

    if active_bookings_count >= flight_instance.capacity:
        raise BookingError("Flight is fully booked.")

    booking = Booking.objects.create(
        user=user,
        flight_instance=flight_instance,
        status=Booking.STATUS_PENDING,
    )

    return booking

def cancel_booking(*, booking: Booking, user) -> Booking:
    # Permission: owner or staff
    if booking.user_id != user.id and not user.is_staff:
        raise PermissionDenied("You do not have permission to cancel this booking.")

    # Idempotent cancel
    if booking.status == "cancelled":
        return booking

    with transaction.atomic():
        booking.status = "cancelled"
        booking.save(update_fields=["status"])
    return booking