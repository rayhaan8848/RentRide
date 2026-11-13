from django.urls import path
from .views import *

urlpatterns = [
     path('categories/', home, name='home'),
]
