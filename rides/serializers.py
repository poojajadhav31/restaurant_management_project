from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rider, Driver
from .models import Ride

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RiderRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Rider
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "preferred_payment_method",
            "default_pickup_location",
            "profile_photo",
        ]

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create Rider profile
        rider = Rider.objects.create(user=user, **validated_data)
        return rider


class DriverRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Driver
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "vehicle_make",
            "vehicle_model",
            "vehicle_number_plate",
            "driver_license_number",
            "profile_photo",
        ]

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create Driver profile
        driver = Driver.objects.create(user=user, **validated_data)
        return driver

class RideSerializer(serializers.ModelSerializer):
    rider = serializers.StringRelatedField()
    driver = serializers.StringRelatedField()

    class Meta:
        model = Ride
        fields = ["id", "rider", "driver", "pickup_location", "dropoff_location", "status", "created_at"]