from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction


from accounts.models import User
from accounts.views import role_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Vehicle, Category, VehicleImage, Location

from .models import Vehicle, Category, VehicleImage
from .forms import VehicleForm
from .filters import filter_vehicles


def home(request):

    categories = Category.objects.filter(is_active=True)

    locations = Location.objects.filter(is_active=True)

    vehicles = filter_vehicles(request)

    context = {
        'categories': categories,
        'locations': locations,
        'vehicles': vehicles,
    }

    return render(request, 'main/home.html', context)


# Add Vehicle
@login_required
@role_required(User.Role.OWNER)
def add_vehicle(request):

    if request.method == 'POST':

        form = VehicleForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            additional_images = request.FILES.getlist(
                'additional_images'
            )

            try:
                with transaction.atomic():

                    vehicle = form.save(commit=False)

                    vehicle.owner = request.user

                    vehicle.approval_status = (
                        Vehicle.ApprovalStatus.PENDING
                    )

                    vehicle.save()

                    for image in additional_images:
                        VehicleImage.objects.create(
                            vehicle=vehicle,
                            image=image
                        )

                messages.success(
                    request,
                    'Vehicle submitted successfully! '
                    'Waiting for admin approval.'
                )

                return redirect('owner_dashboard')

            except Exception:
                messages.error(
                    request,
                    'Something went wrong while saving your vehicle.'
                )

        else:
            messages.error(
                request,
                'Please correct the errors in the form.'
            )

    else:
        form = VehicleForm()

    context = {
        'form': form
    }

    return render(
        request,
        'rentals/add_vehicle.html',
        context
    )
# Owner - My Vehicles
@login_required
@role_required(User.Role.OWNER)
def my_vehicles(request):

    vehicles = Vehicle.objects.filter(
        owner=request.user
    ).select_related('category').prefetch_related('images')

    context = {
        'vehicles': vehicles
    }

    return render(
        request,
        'rentals/my_vehicles.html',
        context
    )
# Edit Vehicle
@login_required
@role_required(User.Role.OWNER)
def edit_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        owner=request.user
    )

    if request.method == 'POST':

        form = VehicleForm(
            request.POST,
            request.FILES,
            instance=vehicle
        )

        if form.is_valid():

            additional_images = request.FILES.getlist(
                'additional_images'
            )

            with transaction.atomic():

                updated_vehicle = form.save(commit=False)

                # Keep the original owner
                updated_vehicle.owner = request.user

                # Require admin approval after editing
                updated_vehicle.approval_status = (
                    Vehicle.ApprovalStatus.PENDING
                )

                updated_vehicle.save()

                # Save newly uploaded additional images
                for image in additional_images:
                    VehicleImage.objects.create(
                        vehicle=updated_vehicle,
                        image=image
                    )

            messages.success(
                request,
                'Vehicle updated successfully! '
                'It is now waiting for admin approval.'
            )

            return redirect('my_vehicles')

    else:
        form = VehicleForm(instance=vehicle)

    context = {
        'form': form,
        'vehicle': vehicle,
    }

    return render(
        request,
        'rentals/edit_vehicle.html',
        context
    )
# Delete Vehicle
@login_required
@role_required(User.Role.OWNER)
@require_POST
def delete_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        owner=request.user
    )

    vehicle.delete()

    messages.success(
        request,
        'Vehicle deleted successfully.'
    )

    return redirect('my_vehicles')

# Admin - View Pending Vehicles
@login_required
@role_required(User.Role.ADMIN)
def admin_vehicle_approvals(request):

    vehicles = Vehicle.objects.filter(
        approval_status=Vehicle.ApprovalStatus.PENDING
    ).select_related(
        'owner',
        'category'
    ).prefetch_related('images').order_by('-created_at')

    context = {
        'vehicles': vehicles,
    }

    return render(
        request,
        'rentals/admin_vehicle_approvals.html',
        context
    )


# Admin - Approve Vehicle
@login_required
@role_required(User.Role.ADMIN)
@require_POST
def approve_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        approval_status=Vehicle.ApprovalStatus.PENDING
    )

    vehicle.approval_status = Vehicle.ApprovalStatus.APPROVED
    vehicle.save()

    messages.success(
        request,
        f'{vehicle.brand} {vehicle.name} has been approved.'
    )

    return redirect('admin_vehicle_approvals')


# Admin - Reject Vehicle
@login_required
@role_required(User.Role.ADMIN)
@require_POST
def reject_vehicle(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle,
        id=vehicle_id,
        approval_status=Vehicle.ApprovalStatus.PENDING
    )

    vehicle.approval_status = Vehicle.ApprovalStatus.REJECTED
    vehicle.save()

    messages.warning(
        request,
        f'{vehicle.brand} {vehicle.name} has been rejected.'
    )

    return redirect('admin_vehicle_approvals')

# ==========================================
# VEHICLE DETAIL
# ==========================================

def vehicle_detail(request, vehicle_id):

    vehicle = get_object_or_404(
        Vehicle.objects.select_related(
            'category',
            'owner'
        ).prefetch_related('images'),
        id=vehicle_id,
        is_available=True,
        approval_status=Vehicle.ApprovalStatus.APPROVED,
        category__is_active=True
    )

    context = {
        'vehicle': vehicle,
    }

    return render(
        request,
        'rentals/vehicle_detail.html',
        context
    )