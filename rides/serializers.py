from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Rider, Driver
from .models import Ride, RideFeedback

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
    
class DriverLocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["current_latitude", "current_longitude"]
        
from rest_framework import serializers
from .models import Ride

class RideHistorySerializer(serializers.ModelSerializer):
    driver = serializers.CharField(source="driver.username", read_only=True)
    rider = serializers.CharField(source="rider.username", read_only=True)

    class Meta:
        model = Ride
        fields = ["pickup", "drop", "status", "requested_at", "driver", "rider"]


class RideFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideFeedback
        fields = ["id", "ride", "rating", "comment", "is_driver", "submitted_at"]
        read_only_fields = ["id", "submitted_at", "is_driver"]

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        ride = data.get("ride")

        # 1. Ensure ride exists
        if not ride:
            raise serializers.ValidationError({"ride": "Ride is required."})

        # 2. Ride must be completed
        if ride.status != "COMPLETED":
            raise serializers.ValidationError("Ride is not completed yet.")

        # 3. User must belong to the ride (either rider or driver)
        if ride.rider != user and ride.driver != user:
            raise serializers.ValidationError("You are not part of this ride.")

        # 4. Check if feedback already exists for this user+ride
        if RideFeedback.objects.filter(ride=ride, submitted_by=user).exists():
            raise serializers.ValidationError("Feedback already submitted for this ride.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        ride = validated_data["ride"]

        # determine if feedback is from driver or rider
        is_driver = True if ride.driver == user else False

        feedback = RideFeedback.objects.create(
            ride=ride,
            submitted_by=user,
            rating=validated_data["rating"],
            comment=validated_data.get("comment", ""),
            is_driver=is_driver
        )
        return feedback