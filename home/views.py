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


def menu_list_view(request):
    menu_items = [
        "name" : "Panner Tikka", "description":"Grilled cottage cheese with spices","price":150},
        "name" : "Veg Biryani", "description":"Aromatic rice with vegetables and spices", "price":180},
        "name" :  "Butter Chiken","description":"Creamy chiken curry","price":220},
    ]    

    return render(request,"home/menu_list.html", {"menu_items":,menu_items})

def contact_view(request):
    return render(request, "home/contact.html")