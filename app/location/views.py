"""
Views for the location APIs
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.models import Location
from location import serializers


class LocationViewSet(viewsets.ModelViewSet):
    """View for manage location APIs."""
    serializer_class = serializers.LocationSerializer
    queryset = Location.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve locations for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

