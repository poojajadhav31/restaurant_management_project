import requests
from django.shortcuts import render

def homepage_view(request):
    try:
        response = requests.get("http://localhost:8000/api/products/")
        menu_items = response.json()
    except:
        menu_items= []
    return render(requests, "home/menu.html", {"menu_items":menu_items})

def custom_404_view(request, exception):
    return render(request, 'home/404.html', staus=404)