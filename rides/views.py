from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .serializers import RiderRegistrationSerializer, DriverRegistrationSerializer


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

class RideListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated and can see ride details!"})