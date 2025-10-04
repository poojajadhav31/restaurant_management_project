from django.db import models
from django.contrib.auth.models import User
from products.models import Product   
from django.utils import timezone
from datetime import timedelta

class ActiveOrderManager(models.Manager):
    def get_active_orders(self):
        # Filter orders with status 'pending' or 'processing'
        return self.filter(status__in=['pending', 'processing','active'])

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    objects = ActiveOrderManager()  # <-- Attach your custom manager here

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} * {self.product.name}"

def default_valid_until():
    return timezone.now().date() + timedelta(days=30)

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateField(default=timezone.now)  # default is a callable
    valid_until = models.DateField(default=default_valid_until)  # use a callable for default

    def __str__(self):
        return self.code
