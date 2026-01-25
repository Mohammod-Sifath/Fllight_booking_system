from django.urls import path
from apps.common.views import health
from apps.inventory.api import availability_list

urlpatterns = [
    path("health/", health, name="health"),
    path("availability/", availability_list, name="availability-list"),
]
