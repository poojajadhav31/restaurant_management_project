from django.urls import path
from . import views

urlpatterns = [
    path("register/rider/", views.register_rider, name="register_rider"),
    path("register/driver/", views.register_driver, name="register_driver"),
]
