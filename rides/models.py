from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Rider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rider_profile")
    phone_number = models.CharField(max_length=15, unique=True)
    preferred_payment_method = models.CharField(max_length=50, blank=True, null=True)
    default_pickup_location = models.CharField(max_length=255, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="riders/profile_photos/", blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"Rider: {self.user.username}"


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    phone_number = models.CharField(max_length=15, unique=True)
    vehicle_make = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_number_plate = models.CharField(max_length=20, unique=True)
    driver_license_number = models.CharField(max_length=50, unique=True)
    availability_status = models.BooleanField(default=True)
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="drivers/profile_photos/", blank=True, null=True)
    rating = models.FloatField(default=0.0)
    last_ride_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Driver: {self.user.username} - {self.vehicle_number_plate}"

class Ride(models.Model):
    STATUS_CHOICES = [
        ("REQUESTED", "Requested"),
        ("ONGOING", "Ongoing"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)

    pickup_address = models.CharField(max_length=255)
    dropoff_address = models.CharField(max_length=255)

    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()
    drop_lat = models.FloatField()
    drop_lng = models.FloatField()

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="REQUESTED")

    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return f"Ride {self.id} - {self.status}"
    
    
class RideFeedback(models.Model):
    ride = models.ForeignKey("Ride", on_delete=models.CASCADE, related_name="feedbacks")
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    is_driver = models.BooleanField()  # True if driver left feedback
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("ride", "submitted_by")  # one feedback per user per ride

    def __str__(self):
        return f"Feedback by {self.submitted_by.username} on Ride {self.ride.id}"
