
from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):

    # ==================================
    # USER ROLES
    # ==================================

    class Role(models.TextChoices):

        CUSTOMER = "customer", "Customer"
        OWNER = "owner", "Vehicle Owner"
        ADMIN = "admin", "Admin"


    # ==================================
    # BASIC INFORMATION
    # ==================================

    fullname = models.CharField(
        max_length=50,
        blank=True
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )


    # ==================================
    # PROFILE INFORMATION
    # ==================================

    profile_image = CloudinaryField(
        "images",
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True
    )


    # ==================================
    # ROLE MANAGEMENT
    # ==================================

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CUSTOMER
    )


    # ==================================
    # STRING REPRESENTATION
    # ==================================

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
