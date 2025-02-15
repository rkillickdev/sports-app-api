"""
Views for the location APIs
"""

from rest_framework import viewsets
from rest_framework import permissions

from core.models import (
    Location,
    Reservation,
)
from location import serializers


class LocationViewSet(viewsets.ModelViewSet):
    """View for manage location APIs."""

    serializer_class = serializers.LocationDetailSerializer
    queryset = Location.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # def get_queryset(self):
    #     """Retrieve locations for authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for requests."""
        if self.action == "list":
            return serializers.LocationSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new location."""
        serializer.save(user=self.request.user)


class ReservationViewSet(viewsets.ModelViewSet):
    """View for manage reservation APIs."""

    serializer_class = serializers.ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Create a new reservation."""
        serializer.save(created_by=self.request.user)
