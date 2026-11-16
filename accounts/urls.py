from django.urls import path
from .views import *

urlpatterns = [
   path('signup/', user_register,name="signup"),
   path('log_in/', log_in,name="log_in"),
]
