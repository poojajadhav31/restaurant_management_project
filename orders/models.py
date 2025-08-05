from django.db import models
from django.contrib.auth.models import User
from accounts.models import Customer
from menu.models imporrt Product 

ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('preparing','Preparing'),
    ('ready','Ready'),
    ('completed','Completed'),
    ('cancelled','Cancelled'),
]


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orderss')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='guest_orders')

        items = models.ManyToManyField(Product, related_name='product_orders')
        total_amount = models.DecimalField(max_digits=10, decimal_places=2)
        status = models.CharField(
        max_length=20,
        choices-ORDER_STATUS_CHOICES,
        default='pending')

        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Order#{self.id} - rs{self.total_amount}"
