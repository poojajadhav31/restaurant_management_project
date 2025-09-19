# orders/utils.py
import string
import secrets

from .models import Coupon  # assumes you will (or already) have a Coupon model

def generate_coupon_code(length=10):
    """
    Generate a unique alphanumeric coupon code.

    Args:
        length (int): The length of the coupon code (default is 10).

    Returns:
        str: A unique coupon code string.
    """
    characters = string.ascii_uppercase + string.digits

    while True:
        # Generate a random alphanumeric code
        code = ''.join(secrets.choice(characters) for _ in range(length))

        # Ensure uniqueness by checking the DB
        if not Coupon.objects.filter(code=code).exists():
            return code
