from django.urls import path
from .views import (
    register_rider,
    register_driver,
    RideRequestView,
    AvailableRidesView,
    AcceptRideView,
    RideListView,
)

urlpatterns = [
    path("", RideListView.as_view(), name="ride-list"),  # fixed as_view()
    path("register-rider/", register_rider, name="register_rider"),
    path("register-driver/", register_driver, name="register_driver"),
    path("ride/request/", RideRequestView.as_view(), name="ride-request"),
    path("ride/available/", AvailableRidesView.as_view(), name="available-rides"),
    path("ride/accept/<int:ride_id>/", AcceptRideView.as_view(), name="accept-ride"),
]
