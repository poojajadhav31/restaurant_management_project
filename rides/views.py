from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .serializers import RiderRegistrationSerializer, DriverRegistrationSerializer , RideSerializer
from .models import Rider, Driver, Ride

# ---------------- Rider & Driver Registration ---------------- #
@api_view(["POST"])
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
