
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from django.views.decorators.http import require_POST

from accounts.models import User
from accounts.views import role_required

from rentals.models import Vehicle

from .forms import BookingForm
from .models import Booking


# ==========================================
# CREATE BOOKING
# ==========================================

@login_required
@role_required(User.Role.CUSTOMER)
def create_booking(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        is_available=True,
        approval_status=Vehicle.ApprovalStatus.APPROVED,
        category__is_active=True
    )

    if request.method == 'POST':

        form = BookingForm(request.POST)

        if form.is_valid():

            pickup_date = form.cleaned_data['pickup_date']
            return_date = form.cleaned_data['return_date']

            # CHECK PICKUP DATE
            if pickup_date < timezone.localdate():

                form.add_error(
                    'pickup_date',
                    'Pickup date cannot be in the past.'
                )

            # CHECK RETURN DATE
            if return_date <= pickup_date:

                form.add_error(
                    'return_date',
                    'Return date must be after pickup date.'
                )

            # CHECK VEHICLE AVAILABILITY
            if not form.errors:

                with transaction.atomic():

                    # Lock the vehicle row while checking availability
                    locked_vehicle = get_object_or_404(
                        Vehicle.objects.select_for_update(),
                        id=vehicle_id,
                        is_available=True,
                        approval_status=Vehicle.ApprovalStatus.APPROVED,
                        category__is_active=True
                    )

                    # Find overlapping pending or accepted bookings
                    conflicting_bookings = Booking.objects.filter(
                        vehicle=locked_vehicle,
                        status__in=[
                            Booking.Status.PENDING,
                            Booking.Status.ACCEPTED,
                        ],
                        pickup_date__lt=return_date,
                        return_date__gt=pickup_date,
                    )

                    if conflicting_bookings.exists():

                        form.add_error(
                            None,
                            'Sorry! This vehicle is already booked for the selected dates. Please choose different dates.'
                        )

                    else:

                        # CALCULATE RENTAL PRICE
                        rental_days = (
                            return_date - pickup_date
                        ).days

                        daily_price = locked_vehicle.daily_price

                        total_price = daily_price * rental_days

                        # SAVE BOOKING
                        booking = form.save(commit=False)

                        booking.customer = request.user
                        booking.vehicle = locked_vehicle
                        booking.daily_price = daily_price
                        booking.total_price = total_price
                        booking.status = Booking.Status.PENDING

                        booking.save()

                # SUCCESS MESSAGE
                if not form.errors:

                    messages.success(
                        request,
                        'Your booking request has been submitted successfully!'
                    )

                    return redirect(
                        'vehicle_detail',
                        vehicle_id=vehicle.id
                    )

    else:

        form = BookingForm()

    context = {
        'form': form,
        'vehicle': vehicle,
    }

    return render(
        request,
        'booking/create_booking.html',
        context
    )

# ==========================================
# CUSTOMER - MY BOOKINGS
# ==========================================

@login_required
@role_required(User.Role.CUSTOMER)
def my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related(
        'vehicle',
        'vehicle__category'
    ).order_by('-created_at')

    context = {
        'bookings': bookings,
    }

    return render(
        request,
        'booking/my_bookings.html',
        context
    )

# ==========================================
# OWNER - MANAGE BOOKINGS
# ==========================================

@login_required
@role_required(User.Role.OWNER)
def owner_bookings(request):

    bookings = Booking.objects.filter(
        vehicle__owner=request.user
    ).select_related(
        'customer',
        'vehicle',
        'vehicle__category'
    ).order_by('-created_at')

    context = {
        'bookings': bookings,
    }

    return render(
        request,
        'booking/owner_bookings.html',
        context
    )

# ==========================================
# OWNER - ACCEPT BOOKING
# ==========================================

@login_required
@role_required(User.Role.OWNER)
@require_POST
def accept_booking(request, booking_id):

    with transaction.atomic():

        booking = get_object_or_404(
            Booking.objects.select_related('vehicle'),
            id=booking_id,
            vehicle__owner=request.user,
            status=Booking.Status.PENDING
        )

        # Lock vehicle to protect availability checks
        vehicle = get_object_or_404(
            Vehicle.objects.select_for_update(),
            id=booking.vehicle_id
        )

        # Check for another overlapping booking
        conflicting_bookings = Booking.objects.filter(
            vehicle=vehicle,
            status__in=[
                Booking.Status.PENDING,
                Booking.Status.ACCEPTED
            ],
            pickup_date__lt=booking.return_date,
            return_date__gt=booking.pickup_date
        ).exclude(
            id=booking.id
        )

        if conflicting_bookings.exists():

            messages.error(
                request,
                'Cannot accept this booking because another booking conflicts with these dates.'
            )

        else:

            booking.status = Booking.Status.ACCEPTED
            booking.save(update_fields=['status', 'updated_at'])

            messages.success(
                request,
                'Booking accepted successfully!'
            )

    return redirect('owner_bookings')


# ==========================================
# OWNER - REJECT BOOKING
# ==========================================

@login_required
@role_required(User.Role.OWNER)
@require_POST
def reject_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        vehicle__owner=request.user,
        status=Booking.Status.PENDING
    )

    booking.status = Booking.Status.REJECTED
    booking.save(update_fields=['status', 'updated_at'])

    messages.success(
        request,
        'Booking rejected successfully.'
    )

    return redirect('owner_bookings')

# ==========================================
# CUSTOMER - CANCEL BOOKING
# ==========================================

@login_required
@role_required(User.Role.CUSTOMER)
@require_POST
def cancel_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        customer=request.user,
        status=Booking.Status.PENDING
    )

    booking.status = Booking.Status.CANCELLED
    booking.save(update_fields=['status', 'updated_at'])

    messages.success(
        request,
        'Your booking has been cancelled successfully.'
    )

    return redirect('my_bookings')

