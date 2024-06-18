"""
Serializers for location APIs
"""
from rest_framework import serializers

from core.models import Location


class LocationSerializer(serializers.ModelSerializer):
  """Serializer for ocations."""

  class Meta:
    model = Location
    fields = ['id', 'name', 'summary', 'latitude', 'longitude']
    read_only_fields = ['id']