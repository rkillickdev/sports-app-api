"""
URL mappings for the location app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from location import views


router = DefaultRouter()
router.register('locations', views.LocationViewSet)
router.register('reservations', views.ReservationViewSet)

app_name = 'location'

urlpatterns = [
    path('', include(router.urls)),
]