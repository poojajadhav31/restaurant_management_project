from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import Order, Coupon
from .serializers import OrderSerializer, CouponSerializer
from rest_framework import status
from django.utils import timezone

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_order_list(request):
    # Return serialized orders for the authenticated user
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
    
class CouponValidationView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code", "").strip()

        try:
            coupon = Coupon.objects.get(code__iexact=code)
        except Coupon.DoesNotExist:
            return Response({"error": "Invalid coupon code."}, status=status.HTTP_400_BAD_REQUEST)

        today = timezone.now().date()
        if not coupon.is_active or coupon.valid_from > today or coupon.valid_until < today:
            return Response({"error": "Coupon is not valid."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CouponSerializer(coupon)
        return Response({"success": True, "discount": serializer.data}, status=status.HTTP_200_OK)
