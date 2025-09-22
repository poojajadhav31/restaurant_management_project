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
    RiderHistoryView, DriverHistoryView, RideFeedbackView, CalculateFareAPIView, FareCalculationView ,RidePaymentView,
    mark_ride_payment
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
    path("rides/<int:pk>/calculate-fare/", FareCalculationView.as_view(), name="calculate-fare"),
    path("ride/calculate-fare/<int:ride_id>/", CalculateFareAPIView.as_view(), name="calculate-fare"),
    path("ride/payment/<int:ride_id>/", RidePaymentView.as_view(), name="ride-payment"),
    path("payment/<int:ride_id>/", mark_ride_payment, name="ride-payment"),


    # New Ride History APIs
    path("rider/history/", RiderHistoryView.as_view(), name="rider-history"),
    path("driver/history/", DriverHistoryView.as_view(), name="driver-history"),
    path("ride/feedback/<int:ride_id>/", RideFeedbackView.as_view(), name="ride-feedback"),
]

