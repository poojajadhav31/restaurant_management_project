from django.contrib import admin
from .models import RestaurantInfo
from .models import RestaurantLocation
from .models import ContactSubmission
from .models import Feedback

# Register your models here.
@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ("name", "address", 'phone_number')

admin.site.register(RestaurantLocation)
admin.site.register(ContactSubmission)
admin.site.register(Feedback)
opening_hours = "Mon-Fri: 11 AM-9PM\nSat-Sun: 10AM-10PM"
