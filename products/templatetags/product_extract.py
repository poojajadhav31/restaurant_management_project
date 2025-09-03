from django import template

register = template.Library()

@register.filter
def show_availability(product):
    """
    If product is unavailable, show 'Coming Soon',
    else return the product name.
    """
    if not product.available:
        return f"{product.name} - Coming Soon "
    return product.name
