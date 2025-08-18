import logging
import requests
from django.conf import settings
from django.shortcuts import render
from .forms import  ContactForm
from products.models import Product
from django import feedbackform
from .models import feedback
from .models import RestaurantInfo

# congigure logger
logger = logging.getLogger(__name__)

def homepage_view(request):
    try:
        api_url = "http://localhost:8000/api/products/"
        response = requests.get(api_url, timeout=5)
        response.raise_for_status() # Raise HTTPERROR for response
        restaurant_menu_items = response.json()
    except requests.exceptions.RequestException as e:
        logger.exception("Failed to fetch restaurant menu from API.")
        restaurant_menu_items= []

    # Fetch restuarant address from model
    restuarant = RestaurantInfo.objects.first()
    address = restaurant.address if restaurant else "Address not available"

    return render(
        request,
        "home/menu.html", 
        {
        "restaurant_menu_items":restaurant_menu_items,
        "restaurant_name" :getattr(settings , "RESTAURANT_NAME"),
        "restaurant_phone" :getattr(settings,"RESTAURANT_PHONE"),
        "restaurant_address" : address,
        }
    )

def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)


def menu_view(request):
    menu_items = Product.objects.all()
    return render(request,"home/menu.html", {
        "menu_items":,menu_items,
        "restaurant_name":"Tasty Bites"
    })

def contact_view(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        return render(request,"home/contact_success.html",{})
    return render(request, "home/contact.html",{"form":form})

def rservations_view(request):
    return render(request,"home/reservations.html",{
        "restaurant_name" : settings.RESTAURANT_NAME,
        "restaurant_phone" : settings.RESTAURANT_PHONE
        })

# feedbackform view

class feedbackform(forms.ModelForm):
    class Meta:
        model = feedback
        fields = ["comments"]

def feedback_view(request):
    if request.method == "POST":
        form = feedbackform(render.POST)
        if form.is_valid():
            form.save()
            return render(request, "home/feedback_thanks.html")
    else:
        form = feedbackform()
    return render(request, "home/feedback.html,{"form":form})
