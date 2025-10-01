from django.urls import path
from .views import OrderHistoryView, protected_order_list, CouponValidationView

urlpatterns = [
    path('', protected_order_list, name="orders"),
    path("history/", OrderHistoryView.as_view(), name="order-history"),
    path('coupons/validate/', CouponValidationView.as_view(), name='coupon-validate'),
]