from django.contrib import admin
from .models import Product


# Custom Admins
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','created_at']


# Register your models here.
admin.site.register(Product, ProductAdmin)