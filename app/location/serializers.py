"""
Serializers for location APIs
"""
from rest_framework import serializers

from core.models import (
    Location,
    Reservation,
)

from user.serializers import UserDetailSerializer


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for locations."""

    class Meta:
        model = Location
        fields = ['id', 'address', 'name', 'image']
        read_only_fields = ['id']


class LocationDetailSerializer(LocationSerializer):
    """Serializer for location detail view"""
    user = UserDetailSerializer(read_only=True, many=False)
    class Meta(LocationSerializer.Meta):
        fields = LocationSerializer.Meta.fields + ['summary', 'user']


class ReservationSerializer(serializers.ModelSerializer):
    """Serializer for reservations."""
    created_by = UserDetailSerializer(read_only=True, many=False)
    location = LocationDetailSerializer(read_only=True, many=False)
    class Meta:
        model = Reservation
        fields = ['id', 'date_time', 'created_by', 'location', 'created_at']