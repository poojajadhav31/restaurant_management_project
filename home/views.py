import logging
import requests
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from products.models import Product
from .models import RestaurantInfo, ContactSubmission,feedback
from .forms import ContactForm ,FeedbackForm

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
    hours = restaurant.opening_hours if restaurant else "No opening hours available"
    logo = restaurant.logo.url if restaurant and restaurant.logo else None

    cart_count = 0
    if request.user.is_authenticated:
        try:
            pending_order = Order.objects.get(user=request.user, status='pending')
            cart_count = pending_order.items.count()
        except Order.DoesNotExist:
            cart_count = 0

    return render(
        request,
        "home/menu.html", 
        {
        "restaurant_menu_items":restaurant_menu_items,
        "restaurant_name" :getattr(settings , "RESTAURANT_NAME"),
        "restaurant_phone" :getattr(settings,"RESTAURANT_PHONE"),
        "restaurant_address" : address,
        "opening_hours" : hours,
        "restaurant_logo" :logo,
        "cart_count": cart_count
        "breadcrumbs":[("Home", None)],
        }
    )

def about_view(request):
    restuarant_info = RestaurantInfo.objects.first()
    return render(request, "home/about.html",{'restuarant_info':restuarant_info}),{
        "breadcrumbs": [
            ("Home", "/"),
            ("About", None)
        ],
    })

def custom_404_view(request, exception):
    return render(request, 'home/404.html', status=404)


def menu_view(request):
    menu_items = Product.objects.all()
    return render(request,"home/menu.html", {
        "menu_items":,menu_items,
        "restaurant_name":"Tasty Bites"
        "breadcrumbs": [
            ("Home", "/")
            ("Menu", None)
        ],
    })

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            ContactSubmission.objects.create(
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email']
            )
            return render(request,"home/contact_success.html",{})
        else:
            form = ContactForm
    return render(request, "home/contact.html",{"form":form}),
        "form": form,
        "breadcrumbs":[
            ("Home", "/")
            ("Contact",None)
        ],
    })
     
def email_contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = f" New Contact Message from {name}"
            body = f"Name: {name}\nEmail: {email}\n{message}"

            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['your_resaturant@gmail.com'],
            )

            return render(request, 'home/email_success.html')
    else:
        form = ContactForm()
    
    return render(request,'home/contact.html', {'form': from})
    

def reservations_view(request):
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

def privacy_policy(request):
    return render(request, 'privacy_policy.html')