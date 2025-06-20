from django.urls import path
from .views import FitnessClassList, BookClass, BookingList

urlpatterns = [
    path('classes/', FitnessClassList.as_view(),name='classes'),
    path('book/', BookClass.as_view(),name='book'),
    path('bookings/', BookingList.as_view(),name='bookings'), # using query parameters for example http://127.0.0.1:8000/bookings/?email=dinesh@example.com
    #path('bookings/<str:email>/', BookingList.as_view()), #this one is path parameter we need to pass this email into the view
]
