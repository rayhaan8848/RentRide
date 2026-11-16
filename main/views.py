from django.shortcuts import render
from rentals.models import Category, Location, Vehicle


def home(request):
    categories = Category.objects.filter(is_active=True).order_by('name')
    locations = Location.objects.filter(is_active=True)
    vehicles = Vehicle.objects.filter(
        is_available=True,
        category__is_active=True,
    ).select_related('category').order_by('daily_price', 'name')

    return render(request, 'main/home.html', {
        'categories': categories,
        'locations': locations,
        'vehicles': vehicles,
    })