from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from apps.bookings.models import Booking
from apps.bookings.services import BookingError, create_booking
from apps.inventory.models import Flight, FlightInstance


class CreateBookingTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="u1", password="pass12345")

        self.flight = Flight.objects.create(code="AY123", origin="HEL", destination="ARN")

        departure = timezone.now() + timedelta(days=1)
        arrival = departure + timedelta(hours=1)

        self.instance = FlightInstance.objects.create(
            flight=self.flight,
            departure_at=departure,
            arrival_at=arrival,
            capacity=1,
            base_price_cents=10000,
            is_active=True,
        )

    def test_create_booking_when_capacity_available(self):
        booking = create_booking(user=self.user, flight_instance_id=self.instance.id)
        self.assertEqual(booking.status, Booking.STATUS_PENDING)

    def test_create_booking_raises_when_full(self):
        create_booking(user=self.user, flight_instance_id=self.instance.id)
        with self.assertRaises(BookingError):
            create_booking(user=self.user, flight_instance_id=self.instance.id)
