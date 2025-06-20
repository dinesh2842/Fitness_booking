from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import FitnessClass, Booking
from django.utils import timezone
from datetime import timedelta


class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a fitness class
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            instructor="Alice",
            datetime=timezone.now() + timedelta(days=1),
            available_slots=2,
        )
        self.book_url = reverse('book')  # make sure your path('book/', ...) is named 'book'
        self.classes_url = reverse('classes')  # similarly, path('classes/', ...) named 'classes'
        self.bookings_url = reverse('bookings')  # path('bookings/', ...) named 'bookings'

    def test_list_classes(self):
        """Test GET /classes/ returns fitness classes"""
        resp = self.client.get(self.classes_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp.data) > 0)
        self.assertEqual(resp.data[0]['name'], "Yoga")

    def test_successful_booking(self):
        """Test POST /book/ decreases available slots and returns booking data"""
        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Alice Smith",
            "client_id": 123,
            "client_email": "alice@example.com"
        }
        resp = self.client.post(self.book_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        booking = Booking.objects.get(client_email="alice@example.com")
        self.assertEqual(booking.client_name, "Alice Smith")

        # Check that slots decreased
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 1)

    def test_overbooking(self):
        """Test that booking fails when slots are exhausted"""
        self.fitness_class.available_slots = 0
        self.fitness_class.save()

        data = {
            "fitness_class": self.fitness_class.id,
            "client_name": "Bob",
            "client_id": 456,
            "client_email": "bob@example.com"
        }
        resp = self.client.post(self.book_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', resp.data)

    def test_get_bookings(self):
        """Test GET /bookings/?email= returns client bookings"""
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Alice Smith",
            client_id=123,
            client_email="alice@example.com"
        )

        resp = self.client.get(self.bookings_url, {'email': "alice@example.com"})
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]['client_email'], "alice@example.com")

    def test_get_bookings_without_email(self):
        """Test GET /bookings/ returns error if email is missing"""
        resp = self.client.get(self.bookings_url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['error'], "Email is required")
