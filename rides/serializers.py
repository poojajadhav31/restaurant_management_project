from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum, Avg, Count
from .models import Rider, Driver
from .models import Ride, RideFeedback
from .utils import calculate_distance
from datetime import timedelta
from .models import Ride
from decimal import Decimal

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

class FareCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["id", "status", "pickup_lat", "pickup_lng", "drop_lat", "drop_lng", "fare"]

    def update(self, instance, validated_data):
        """
        Custom update: calculate and set fare only if ride is completed.
        """
        # update status if provided
        status = validated_data.get("status", instance.status)
        instance.status = status

        # Only calculate fare if ride is completed and fare not already set
        if status == "COMPLETED" and instance.fare is None:
            # Constants
            base_fare = Decimal("50.00")
            per_km_rate = Decimal("10.00")
            surge_multiplier = Decimal(self.context.get("surge_multiplier", 1.0))

            # Calculate distance
            distance_km = Decimal(calculate_distance(
                instance.pickup_lat,
                instance.pickup_lng,
                instance.drop_lat,
                instance.drop_lng
            ))

            # Apply formula
            fare = base_fare + (distance_km * per_km_rate * surge_multiplier)
            instance.fare = round(fare, 2)

        instance.save()
        return instance
class RideFareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["id", "fare", "payment_status", "payment_method", "paid_at"]

    def update(self, instance, validated_data):
        # Allow payment status updates only if ride is COMPLETED
        if validated_data.get("payment_status") == "PAID":
            if instance.status != "COMPLETED":
                raise serializers.ValidationError("Ride must be COMPLETED before payment.")
            if instance.payment_status == "PAID":
                raise serializers.ValidationError("Payment is already marked as PAID.")
            instance.payment_status = "PAID"
            instance.payment_method = validated_data.get("payment_method")
            instance.paid_at = timezone.now()
        elif validated_data.get("payment_status") == "UNPAID":
            instance.payment_status = "UNPAID"
            instance.payment_method = None
            instance.paid_at = None

        instance.save()
        return instance
  
class RidePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["payment_status", "payment_method"]

    def validate(self, data):
        ride = self.instance

        if ride.status != "COMPLETED":
            raise serializers.ValidationError("Ride must be completed before payment.")

        if ride.payment_status == "PAID":
            raise serializers.ValidationError("Ride already marked as paid.")

        if data.get("payment_status") == "PAID" and not data.get("payment_method"):
            raise serializers.ValidationError("Payment method required if marking as PAID.")

        return data

    def update(self, instance, validated_data):
        payment_status = validated_data.get("payment_status")
        payment_method = validated_data.get("payment_method")

        if payment_status == "PAID":
            instance.payment_status = "PAID"
            instance.payment_method = payment_method
            instance.paid_at = timezone.now()
            instance.save()

        return instance


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
    
class DriverEarningsSerializer(serializers.Serializer):
    total_rides = serializers.IntegerField()
    total_earnings = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_breakdown = serializers.DictField(child=serializers.IntegerField())
    average_fare = serializers.DecimalField(max_digits=10, decimal_places=2)

    @staticmethod
    def for_driver(driver):
        # filter last 7 days
        seven_days_ago = timezone.now() - timedelta(days=7)
        rides = Ride.objects.filter(
            driver=driver,
            status="COMPLETED",
            payment_status="PAID",
            completed_at__gte=seven_days_ago
        )

        total_rides = rides.count()
        total_earnings = rides.aggregate(total=Sum("fare"))["total"] or 0
        average_fare = rides.aggregate(avg=Avg("fare"))["avg"] or 0

        # Payment breakdown (group by method)
        payment_counts = rides.values("payment_method").annotate(count=Count("id"))
        breakdown = {entry["payment_method"]: entry["count"] for entry in payment_counts}

        data = {
            "total_rides": total_rides,
            "total_earnings": total_earnings,
            "payment_breakdown": breakdown,
            "average_fare": average_fare,
        }

        return DriverEarningsSerializer(data).data