from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile
from products.models import Product


class OrderStatus(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_orders'
    )

    items = models.ManyToManyField(Product, related_name='product_orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # 🔹 Instead of choices, link to OrderStatus
    status = models.ForeignKey(
        OrderStatus,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - Rs{self.total_amount}"
