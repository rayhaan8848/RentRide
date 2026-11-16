
from django.urls import path
from . import views


urlpatterns = [

    # ==================================
    # AUTHENTICATION
    # ==================================

    path(
        'signup/',
        views.user_register,
        name='signup'
    ),

    path(
        'log_in/',
        views.log_in,
        name='log_in'
    ),

    path(
        'logout/',
        views.log_out,
        name='logout'
    ),


    # ==================================
    # ROLE-BASED DASHBOARDS
    # ==================================

    path(
        'dashboard/customer/',
        views.customer_dashboard,
        name='customer_dashboard'
    ),

    path(
        'dashboard/owner/',
        views.owner_dashboard,
        name='owner_dashboard'
    ),

    path(
        'dashboard/admin/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

]
