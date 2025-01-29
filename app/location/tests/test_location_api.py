"""Tests for location APIs"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Location

from location.serializers import (
    LocationSerializer,
    LocationDetailSerializer,
)


# LOCATIONS_URL = reverse('location:location-list')
LOCATIONS_URL = "/api/location/locations/"


def detail_url(location_id):
    """Create and return a location detail URL."""
    return reverse("location:location-detail", args=[location_id])


def create_location(user, **params):
    """Create and return a sample location."""
    defaults = {
        "name": "sample location name",
        "summary": "test summary",
        "country": "England",
        "country_code": "ENG",
    }
    defaults.update(params)

    location = Location.objects.create(user=user, **defaults)
    return location


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicLocationAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(LOCATIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateLocationAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="test123")
        self.client.force_authenticate(self.user)

    def test_retrieve_locations(self):
        """Test retrieving a list of locations."""
        create_location(user=self.user)
        create_location(user=self.user)

        res = self.client.get(LOCATIONS_URL)

        locations = Location.objects.all().order_by("-id")
        serializer = LocationSerializer(locations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_location_list_limited_to_user(self):
        """Test list of locations is limited to authenticated user."""
        other_user = create_user(email="other@example.com", password="test123")
        create_location(user=other_user)
        create_location(user=self.user)

        res = self.client.get(LOCATIONS_URL)

        locations = Location.objects.filter(user=self.user)
        serializer = LocationSerializer(locations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_location_detail(self):
        """Test get location detail."""
        location = create_location(user=self.user)

        url = detail_url(location.id)
        res = self.client.get(url)

        serializer = LocationDetailSerializer(location)
        self.assertEqual(res.data, serializer.data)

    def test_create_location(self):
        """Test creating a location."""
        payload = {
            "name": "sample location name",
            "country": "England",
            "longitude": "ENG",
        }
        res = self.client.post(LOCATIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        location = Location.objects.get(id=res.data["id"])
        for k, v in payload.items():
            self.assertEqual(getattr(location, k), v)
        self.assertEqual(location.user, self.user)
