# home/utils.py
from datetime import datetime, time

def is_restaurant_open():
    """
    Checks if the restaurant is currently open based on hardcoded operating hours.
    Returns True if open, False otherwise.
    """

    # Get current day and time
    now = datetime.now()
    current_time = now.time()
    current_day = now.strftime('%A')  # Example: 'Monday', 'Saturday', etc.

    # Define
