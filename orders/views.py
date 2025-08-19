from django.shortcuts import render
from .models import Order

# Create your views here.
def get_cart_item_count(request):
    if request.user.is_authenticated:
        try:
            order = Order.get(user=request.user, status='pending')
            return order.items.count()
        except Order.DoesNotExist:
            return 0
        else:
            return 0
