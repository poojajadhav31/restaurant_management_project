from django import template

register = template.Library()

@register.filter(name="coming_soon")
def coming_soon(is_available):
    """
    Custom filter to display 'Coming Soon' if product is unavailable.
    Usage: {{ product.is_available|coming_soon }}
    """
    return "Coming Soon 🚀" if not is_available else ""
