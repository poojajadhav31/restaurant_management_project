from django.contrib import admin
from .models import Product, Special, Chef


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'available']
    search_fields = ['name']


@admin.register(Special)
class SpecialAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'description', 'price', 'date']
    search_fields = ['item_name']


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ['name', 'bio']
    search_fields = ['name']
