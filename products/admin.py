from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','price','created_at']
    search_fields =['name']


# Register your models here.
admin.site.register(Product, ProductAdmin)