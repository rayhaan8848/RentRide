from django.shortcuts import render
from .models import Vehicle, Category


def home(request):

    categories = Category.objects.filter(is_active=True)

    vehicles = Vehicle.objects.filter(
        is_available=True,
        category__is_active=True
    ).select_related('category')

    context = {
        'categories': categories,
        'vehicles': vehicles,
    }

    return render(request, 'home.html', context)