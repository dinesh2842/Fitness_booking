from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.utils.timezone import make_aware
from datetime import datetime
import pytz

class FitnessClassList(APIView):
    def get(self, request):
        tz_name = request.GET.get('tz', 'Asia/Kolkata')
        try:
            tz = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            return Response({'error': 'Invalid timezone'}, status=400)

        classes = FitnessClass.objects.all()
        data = []
        for cls in classes:
            local_dt = cls.datetime.astimezone(tz)
            data.append({
                'id': cls.id,
                'name': cls.name,
                'instructor': cls.instructor,
                'datetime': local_dt.isoformat(),
                'available_slots': cls.available_slots
            })
        return Response(data)

class BookClass(APIView):
    def post(self, request):
        # Get fields
        fitness_class_id = request.data.get('fitness_class')
        client_name = request.data.get('client_name')
        client_id = request.data.get('client_id')
        client_email = request.data.get('client_email')

        # Validate all fields
        if not all([fitness_class_id, client_name, client_id, client_email]):
            return Response({"error": "Missing fields"}, status=400)

        # Check that class exists
        try:
            fitness_class = FitnessClass.objects.get(id=fitness_class_id)
        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)

        # Check availability
        if fitness_class.available_slots <= 0:
            return Response({"error": "No slots available"}, status=400)

        # Save booking
        booking = Booking.objects.create(
            fitness_class=fitness_class,
            client_name=client_name,
            client_id=client_id,
            client_email=client_email,
        )
        # Reduce slot
        fitness_class.available_slots -= 1
        fitness_class.save()

        return Response(BookingSerializer(booking).data, status=201)

class BookingList(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)

        bookings = Booking.objects.filter(client_email=email)
        return Response(BookingSerializer(bookings, many=True).data)

# class BookingList(APIView):
#     def get(self, request, email):
#         bookings = Booking.objects.filter(client_email=email)
#         return Response(BookingSerializer(bookings, many=True).data)