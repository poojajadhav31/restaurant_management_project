from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin)
list_display = ['name','email', 'phone','created_at']
search_fields =['name','email','phone']


