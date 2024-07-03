"""
Serializers for user
"""

from rest_framework import serializers

from core.models import (
    User,
)

class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user detail view"""
    class Meta:
        model = User
        fields = ['id', 'name']