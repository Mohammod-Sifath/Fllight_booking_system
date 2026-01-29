from django.urls import path
from apps.common.views import health
from apps.inventory.api import availability_list
from apps.bookings.api import booking_create
from apps.bookings.api import booking_create, booking_cancel
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path("health/", health, name="health"),
    path("availability/", availability_list, name="availability-list"),
    path("bookings/", booking_create, name="booking-create"),
    path("bookings/<int:booking_id>/cancel/", booking_cancel, name="booking-cancel"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
