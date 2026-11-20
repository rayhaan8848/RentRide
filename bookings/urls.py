
from django.urls import path
from . import views

urlpatterns = [
    path(
        'create/<int:vehicle_id>/',
        views.create_booking,
        name='create_booking'
    ),

    path(
        'my-bookings/',
        views.my_bookings,
        name='my_bookings'
    ),
    path(
    'owner-bookings/',
    views.owner_bookings,
    name='owner_bookings'
),
path(
    'accept/<int:booking_id>/',
    views.accept_booking,
    name='accept_booking'
),

path(
    'reject/<int:booking_id>/',
    views.reject_booking,
    name='reject_booking'
),
path(
    'cancel/<int:booking_id>/',
    views.cancel_booking,
    name='cancel_booking'
),
]
