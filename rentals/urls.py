
from django.urls import path
from . import views

urlpatterns = [

    path(
        'categories/',
        views.home,
        name='categories'
    ),

    path(
        'add-vehicle/',
        views.add_vehicle,
        name='add_vehicle'
    ),
    path(
        'my-vehicles/',
        views.my_vehicles,
        name='my_vehicles'
    ),
    path(
        'edit-vehicle/<int:vehicle_id>/',
        views.edit_vehicle,
        name='edit_vehicle'
    ),
    path(
    'delete-vehicle/<int:vehicle_id>/',
    views.delete_vehicle,
    name='delete_vehicle'
    ),
    path(
        'admin/vehicle-approvals/',
        views.admin_vehicle_approvals,
        name='admin_vehicle_approvals'
    ),

    path(
        'admin/approve-vehicle/<int:vehicle_id>/',
        views.approve_vehicle,
        name='approve_vehicle'
    ),

    path(
        'admin/reject-vehicle/<int:vehicle_id>/',
        views.reject_vehicle,
        name='reject_vehicle'
    ),
    path(
    'vehicle/<int:vehicle_id>/',
    views.vehicle_detail,
    name='vehicle_detail'
),

]
