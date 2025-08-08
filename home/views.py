import requests
from django.conf import settings
from django.shortcuts import render

def homepage_view(request):
    try:
        response = requests.get("http://localhost:8000/api/products/")
        menu_items = response.json()
    except:
        menu_items= []

    restaurant_name = getattr(settings, "RESTAURANT_NAME", "Tasty Bites")
    return render(requests, "home/menu.html", {
        "menu_items":menu_items,
        "restaurant_name" : restaurant_name,
        })

def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)