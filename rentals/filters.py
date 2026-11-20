from decimal import Decimal, InvalidOperation

from django.db.models import Q

from .models import Vehicle


def filter_vehicles(request):

    vehicles = Vehicle.objects.filter(
        is_available=True,
        approval_status=Vehicle.ApprovalStatus.APPROVED,
        category__is_active=True
    ).select_related(
        'category',
        'owner'
    )

    # Search by vehicle name or brand
    search = request.GET.get('q', '').strip()

    if search:
        vehicles = vehicles.filter(
            Q(name__icontains=search) |
            Q(brand__icontains=search)
        )

    # Filter by category
    category_id = request.GET.get('category', '').strip()

    if category_id.isdigit():
        vehicles = vehicles.filter(
            category_id=int(category_id)
        )

    # Minimum price
    min_price = request.GET.get('min_price', '').strip()

    if min_price:
        try:
            min_price = Decimal(min_price)

            if min_price >= 0:
                vehicles = vehicles.filter(
                    daily_price__gte=min_price
                )

        except InvalidOperation:
            pass

    # Maximum price
    max_price = request.GET.get('max_price', '').strip()

    if max_price:
        try:
            max_price = Decimal(max_price)

            if max_price >= 0:
                vehicles = vehicles.filter(
                    daily_price__lte=max_price
                )

        except InvalidOperation:
            pass

    # Filter by transmission
    transmission = request.GET.get('transmission', '').strip()

    if transmission in ['AUTOMATIC', 'MANUAL']:
        vehicles = vehicles.filter(
            transmission=transmission
        )

    # Filter by number of seats
    seats = request.GET.get('seats', '').strip()

    if seats.isdigit():
        vehicles = vehicles.filter(
            seats=int(seats)
        )

    return vehicles