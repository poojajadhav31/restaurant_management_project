import string
import secrets

# Remove or comment out the import if you don't have a Coupon model yet
# from .models import Coupon

def generate_coupon_code(length=10, model=None):
    """
    Generate a unique alphanumeric coupon code.

    Args:
        length (int): The length of the coupon code (default is 10).
        model (Django Model): The model to check uniqueness against (must have a 'code' field).

    Returns:
        str: A unique coupon code string.
    """
    characters = string.ascii_uppercase + string.digits

    if model is None:
        # If no model is provided, just return a random code (no uniqueness check)
        return ''.join(secrets.choice(characters) for _ in range(length))

    while True:
        code = ''.join(secrets.choice(characters) for _ in range(length))
        if not model.objects.filter(code=code).exists():
            return code