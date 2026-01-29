from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.inventory.models import Flight, FlightInstance
from apps.bookings.models import Booking


User = get_user_model()


class BookingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass12345")
        self.other_user = User.objects.create_user(username="u2", password="pass12345")

        # Make a flight + instance
        self.flight = Flight.objects.create(
            # adjust these field names if your model differs
            code="AY123",
            origin="HEL",
            destination="ARN",
        )
        self.instance = FlightInstance.objects.create(
            flight=self.flight,
            departure_at="2026-01-19T06:00:00Z",
            arrival_at="2026-01-19T07:00:00Z",
            capacity=3,
            base_price_cents=10000,
            is_active=True,
        )

    def auth(self, user):
        """Helper to authenticate API client as a user."""
        self.client.force_authenticate(user=user)

    def test_availability_endpoint_returns_200(self):
        url = reverse("availability-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_booking_returns_201(self):
        self.auth(self.user)
        url = reverse("booking-create")
        res = self.client.post(url, {"flight_instance_id": self.instance.id}, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["flight_instance"], self.instance.id)
        self.assertEqual(res.data["status"], "pending")

    def test_create_booking_when_full_returns_409(self):
        # Fill capacity with active bookings
        Booking.objects.create(user=self.user, flight_instance=self.instance, status="pending")
        Booking.objects.create(user=self.user, flight_instance=self.instance, status="confirmed")
        Booking.objects.create(user=self.user, flight_instance=self.instance, status="pending")

        self.auth(self.user)
        url = reverse("booking-create")
        res = self.client.post(url, {"flight_instance_id": self.instance.id}, format="json")

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_cancel_booking_owner_returns_200_and_sets_cancelled(self):
        booking = Booking.objects.create(
            user=self.user,
            flight_instance=self.instance,
            status="pending",
        )

        self.auth(self.user)
        url = reverse("booking-cancel", kwargs={"booking_id": booking.id})
        res = self.client.post(url, {}, format="json")  # using POST since you allowed POST/PATCH

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        booking.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")

    def test_cancel_booking_non_owner_returns_403(self):
        booking = Booking.objects.create(
            user=self.user,
            flight_instance=self.instance,
            status="pending",
        )

        self.auth(self.other_user)
        url = reverse("booking-cancel", kwargs={"booking_id": booking.id})
        res = self.client.post(url, {}, format="json")

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
