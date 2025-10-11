from django.db.models import Sum
from .models import Order

def get_daily_sales_total(date):
    """
    Calculates the total sales for a specific date.

    Args:
        date (datetime.date): The date for which total sales should be calculated.

    Returns:
        Decimal: The total sales amount for the given date.
    """
    # Filter orders created on the specified date
    orders = Order.objects.filter(created_at__date=date)

    # Aggregate the sum of total_price for the day
    total = orders.aggregate(total_sum=Sum('total_price'))['total_sum']

    # Return 0 if there are no orders for that date
    return total or 0
