from django.contrib import admin
from .models import RestaurantInfo
from .models import RestaurantLocation

# Register your models here.
admin.site.register(RestaurantInfo)
admin.site.register(RestaurantLocation)
opening_hours = "Mon-Fri: 11 AM-9PM\nSat-Sun: 10AM-10PM"
