from django.db import models
from cloudinary.models import CloudinaryField

# Vehicle Categories
class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)

    image = CloudinaryField("images")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Pickup and Return Locations

# Pickup and Return Locations
class Location(models.Model):

    name = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    province = models.CharField(max_length=100)

    image = CloudinaryField(
        "location_image",
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.district}"



# Vehicle Details
class Vehicle(models.Model):

    TRANSMISSION_CHOICES = [
        ('AUTOMATIC', 'Automatic'),
        ('MANUAL', 'Manual'),
    ]

    FUEL_CHOICES = [
        ('PETROL', 'Petrol'),
        ('DIESEL', 'Diesel'),
        ('ELECTRIC', 'Electric'),
        ('HYBRID', 'Hybrid'),
    ]

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='vehicles'
    )

    name = models.CharField(max_length=150)

    brand = models.CharField(max_length=100)

    model_year = models.PositiveIntegerField()

    description = models.TextField()

    daily_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    seats = models.PositiveIntegerField()

    transmission = models.CharField(
        max_length=20,
        choices=TRANSMISSION_CHOICES
    )

    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_CHOICES
    )

    main_image = CloudinaryField("images")

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Multiple Images for One Vehicle
class VehicleImage(models.Model):

    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = CloudinaryField("images")

    def __str__(self):
        return f"{self.vehicle.name} Image"
