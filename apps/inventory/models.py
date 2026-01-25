from django.db import models


class Flight(models.Model):
    code = models.CharField(max_length=20, unique=True)  # e.g. "AY123"
    origin = models.CharField(max_length=3)              # e.g. "HEL"
    destination = models.CharField(max_length=3)         # e.g. "ARN"
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.code} {self.origin}->{self.destination}"


class FlightInstance(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="instances")
    departure_at = models.DateTimeField()
    arrival_at = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=1)
    base_price_cents = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["flight", "departure_at"]),
            models.Index(fields=["departure_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.flight.code} @ {self.departure_at}"
