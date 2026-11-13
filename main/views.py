from django.shortcuts import render
from rentals.models import Location, Vehicle


def home(request):
    locations = Location.objects.filter(is_active=True)
    vehicles = Vehicle.objects.filter(
        is_available=True,
        category__is_active=True,
    ).select_related('category')

    return render(request, 'main/home.html', {
        'locations': locations,
        'vehicles': vehicles,
    })