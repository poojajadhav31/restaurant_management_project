from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from .serializers import FareCalculationSerializer
from .serializers import RidePaymentSerializer, DriverEarningsSerializer
from django.utils import timezone

from .serializers import RiderRegistrationSerializer, DriverRegistrationSerializer , RideSerializer , DriverLocationUpdateSerializer , RideFeedbackSerializer, RideFareSerializer
from .models import Rider, Driver, Ride , RideFeedback

# ---------------- Rider & Driver Registration ---------------- #
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_ride_payment(request, ride_id):
    """
    Mark a ride as PAID with the selected payment method.
    """
    try:
        ride = Ride.objects.get(id=ride_id)
    except Ride.DoesNotExist:
        return Response({"error": "Ride not found."}, status=status.HTTP_404_NOT_FOUND)

    #  Ownership check (only rider, driver, or admin can access)
    user = request.user
    if ride.rider != user and ride.driver != user and not user.is_staff:
        return Response({"error": "Not authorized to update this ride."},
                        status=status.HTTP_403_FORBIDDEN)

    #  Ride must be completed
    if ride.status != "COMPLETED":
        return Response({"error": "Ride is not completed yet."},
                        status=status.HTTP_400_BAD_REQUEST)

    #  Prevent duplicate payments
    if ride.payment_status == "PAID":
        return Response({"error": "Ride is already marked as paid."},
                        status=status.HTTP_400_BAD_REQUEST)

    #  Validate serializer input
    serializer = RidePaymentSerializer(data=request.data, instance=ride)
    if serializer.is_valid():
        serializer.save(paid_at=timezone.now())
        return Response({
            "message": "Payment marked as complete.",
            "status": ride.payment_status,
            "method": ride.payment_method
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_rider(request):
    serializer = RiderRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        rider = serializer.save()
        return Response(
            {
                "message": "Rider registered successfully!",
                "rider": {
                    "id": rider.id,
                    "username": rider.user.username,
                    "email": rider.user.email,
                    "phone_number": rider.phone_number,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_driver(request):
    serializer = DriverRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        driver = serializer.save()
        return Response(
            {
                "message": "Driver registered successfully!",
                "driver": {
                    "id": driver.id,
                    "username": driver.user.username,
                    "email": driver.user.email,
                    "phone_number": driver.phone_number,
                    "vehicle_number_plate": driver.vehicle_number_plate,
                },
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Ride Workflow ---------------- #

class RideRequestView(APIView):
    """Rider books a ride"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            rider = Rider.objects.get(user=request.user)
            serializer.save(rider=rider, status="REQUESTED")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvailableRidesView(APIView):
    """Drivers see all available rides"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        rides = Ride.objects.filter(status="REQUESTED", driver__isnull=True)
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AcceptRideView(APIView):
    """Driver accepts a ride"""
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        driver = Driver.objects.get(user=request.user)
        ride = get_object_or_404(Ride, id=ride_id)

        if ride.status != "REQUESTED" or ride.driver is not None:
            return Response({"error": "Ride already accepted"}, status=status.HTTP_400_BAD_REQUEST)

        ride.driver = driver
        ride.status = "ONGOING"
        ride.save()

        return Response({"message": "Ride accepted successfully!"}, status=status.HTTP_200_OK)


# ---------------- Dummy Auth Test ---------------- #

class RideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated and can see ride details!"})

# ---------------- Driver Location Update & Ride Tracking ---------------- #

class UpdateLocationView(APIView):
    """Driver updates live location"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            driver = Driver.objects.get(user=request.user)
        except Driver.DoesNotExist:
            return Response({"error": "Only drivers can update location"}, status=status.HTTP_403_FORBIDDEN)

        serializer = DriverLocationUpdateSerializer(driver, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Location updated successfully!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TrackRideView(APIView):
    """Rider tracks driver’s location"""
    permission_classes = [IsAuthenticated]

    def get(self, request, ride_id):
        ride = get_object_or_404(Ride, id=ride_id)

        # ensure ride is ongoing
        if ride.status != "ONGOING":
            return Response({"error": "Tracking available only for ongoing rides"}, status=status.HTTP_400_BAD_REQUEST)

        # ensure only assigned rider or driver can track
        if request.user != ride.rider.user and request.user != ride.driver.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        driver = ride.driver
        if not driver or not driver.current_latitude or not driver.current_longitude:
            return Response({"error": "Driver location not available"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "driver_latitude": driver.current_latitude,
            "driver_longitude": driver.current_longitude
        }, status=status.HTTP_200_OK)
        
# ---------------- Ride Completion & Cancellation ---------------- #

class CompleteRideView(APIView):
    """Driver marks a ride as completed"""
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        driver = Driver.objects.get(user=request.user)
        ride = get_object_or_404(Ride, id=ride_id)

        # Rule: Only assigned driver can complete
        if ride.driver != driver:
            return Response({"error": "You are not assigned to this ride."},
                            status=status.HTTP_403_FORBIDDEN)

        # Rule: Ride must be ongoing
        if ride.status != "ONGOING":
            return Response({"error": "Only ongoing rides can be completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        ride.status = "COMPLETED"
        ride.save()
        return Response({"message": "Ride marked as completed."}, status=status.HTTP_200_OK)


class CancelRideView(APIView):
    """Rider cancels a ride"""
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        rider = Rider.objects.get(user=request.user)
        ride = get_object_or_404(Ride, id=ride_id)

        # Rule: Only the booking rider can cancel
        if ride.rider != rider:
            return Response({"error": "You cannot cancel this ride."},
                            status=status.HTTP_403_FORBIDDEN)

        # Rule: Ride must be REQUESTED to cancel
        if ride.status != "REQUESTED":
            return Response({"error": "Cannot cancel a ride that is already ongoing or completed."},
                            status=status.HTTP_400_BAD_REQUEST)

        ride.status = "CANCELLED"
        ride.save()
        return Response({"message": "Ride cancelled successfully."}, status=status.HTTP_200_OK)

#---------------- Payment Processing ---------------- #
class RidePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure only rider, driver, or admin can access
        if request.user != ride.rider.user and request.user != ride.driver.user and not request.user.is_staff:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        serializer = RidePaymentSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Payment recorded successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class DriverEarningsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        driver = request.user
        summary = DriverEarningsSerializer.for_driver(driver)
        return Response(summary)
# ---------------- Ride History & Feedback ---------------- #
class RiderHistoryView(ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        rider = Rider.objects.get(user=self.request.user)
        return Ride.objects.filter(
            rider=rider, 
            status__in=["COMPLETED", "CANCELLED"]
        ).order_by("-requested_at")


# Driver Ride History
class DriverHistoryView(ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        driver = Driver.objects.get(user=self.request.user)
        return Ride.objects.filter(
            driver=driver, status__in=["COMPLETED", "CANCELLED"]
            
        ).order_by("-requested_at")
class FareCalculationView(generics.UpdateAPIView):
    queryset = Ride.objects.all()
    serializer_class = FareCalculationSerializer
    
class CalculateFareAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        # Get the ride or 404
        ride = get_object_or_404(Ride, id=ride_id)

        # Security: Only rider, driver, or admin can calculate fare
        if not (
            request.user.is_superuser
            or (ride.rider.user == request.user)
            or (ride.driver and ride.driver.user == request.user)
        ):
            return Response(
                {"message": "You do not have permission to calculate fare for this ride."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Validation: Ride must be completed
        if ride.status != "COMPLETED":
            return Response(
                {"message": "Ride must be completed before fare calculation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validation: Prevent re-calculation
        if ride.fare:
            return Response(
                {"message": "Fare already set.", "fare": float(ride.fare)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Use serializer to calculate fare
        serializer = RideFareSerializer(ride, data={}, context={"request": request}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"fare": float(ride.fare), "message": "Fare calculated and saved."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        # 1. Fetch the ride
        ride = get_object_or_404(Ride, id=ride_id)

        # 2. Ensure ride is completed
        if ride.status != "COMPLETED":
            return Response(
                {"error": "Ride is not completed yet."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Determine if user is rider or driver
        is_driver = False
        if hasattr(request.user, "driver"):
            if ride.driver != request.user.driver:
                return Response(
                    {"error": "You are not the driver for this ride."},
                    status=status.HTTP_403_FORBIDDEN
                )
            is_driver = True
        elif hasattr(request.user, "rider"):
            if ride.rider != request.user.rider:
                return Response(
                    {"error": "You are not the rider for this ride."},
                    status=status.HTTP_403_FORBIDDEN
                )
        else:
            return Response(
                {"error": "User is neither rider nor driver."},
                status=status.HTTP_403_FORBIDDEN
            )

        # 4. Check if feedback already exists
        if RideFeedback.objects.filter(ride=ride, submitted_by=request.user, is_driver=is_driver).exists():
            return Response(
                {"error": "You have already submitted feedback for this ride."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. Save feedback
        serializer = RideFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                ride=ride,
                submitted_by=request.user,
                is_driver=is_driver
            )
            return Response(
                {"message": "Feedback submitted successfully."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
