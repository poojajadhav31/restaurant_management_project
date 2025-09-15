from django.urls import path
from .views import (
    register_rider,
    register_driver,
    RideRequestView,
    AvailableRidesView,
    AcceptRideView,
    RideListView,
    UpdateLocationView,
    TrackRideView,
    CompleteRideView, CancelRideView,
    RiderHistoryView, DriverHistoryView
)

urlpatterns = [
    path("", RideListView.as_view(), name="ride-list"),  # fixed as_view()
    path("register-rider/", register_rider, name="register_rider"),
    path("register-driver/", register_driver, name="register_driver"),
    path("ride/request/", RideRequestView.as_view(), name="ride-request"),
    path("ride/available/", AvailableRidesView.as_view(), name="available-rides"),
    path("ride/accept/<int:ride_id>/", AcceptRideView.as_view(), name="accept-ride"),
    path("ride/update-location/", UpdateLocationView.as_view(), name="update-location"),
    path("ride/track/<int:ride_id>/", TrackRideView.as_view(), name="track-ride"),
    path("ride/complete/<int:ride_id>/", CompleteRideView.as_view(), name="complete-ride"),
    path("ride/cancel/<int:ride_id>/", CancelRideView.as_view(), name="cancel-ride"),
    # New Ride History APIs
    path("rider/history/", RiderHistoryView.as_view(), name="rider-history"),
    path("driver/history/", DriverHistoryView.as_view(), name="driver-history"),
]

