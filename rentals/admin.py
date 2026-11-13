from django.contrib import admin

# Register your models here.
from .models import Category, Location, Vehicle, VehicleImage

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Vehicle)
admin.site.register(VehicleImage)