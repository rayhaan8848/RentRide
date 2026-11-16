
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'email',
        'fullname',
        'phone',
        'role',
        'is_active',
        'is_staff',
    )

    list_filter = (
        'role',
        'is_active',
        'is_staff',
    )

    search_fields = (
        'username',
        'email',
        'fullname',
        'phone',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('RentRide Profile', {
            'fields': (
                'fullname',
                'phone',
                'profile_image',
                'address',
                'role',
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('RentRide Information', {
            'fields': (
                'email',
                'fullname',
                'phone',
                'role',
            )
        }),
    )
