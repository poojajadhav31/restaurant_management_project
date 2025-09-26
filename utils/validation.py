# utils/validation_utils.py
from email.utils import parseaddr
import logging

# Configure logging (optional, can be centralized in settings)
logger = logging.getLogger(__name__)

def is_valid_email(email: str) -> bool:
    """
    Validate an email address using Python's built-in email parsing.

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        name, addr = parseaddr(email)
        # A valid email must contain "@" and have something before/after it
        if "@" in addr and "." in addr.split("@")[-1]:
            return True
        return False
    except Exception as e:
        logger.error(f"Email validation error for '{email}': {e}")
        return False
