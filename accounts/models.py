from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField


class User(AbstractUser):

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15, blank=True)

    profile_image = CloudinaryField("images")

    address = models.TextField(blank=True)

    def __str__(self):
        return self.username
