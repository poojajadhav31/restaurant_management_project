from django.urls import path
from .views import menu_api , product_search
from . import views

urlpatterns = [
    path('menu/', menu_api, name='menu-api'),
    path('search/', product_search, name='product-search'),
    path('specials/', views.todays_specials, name='todays-specials'),
    path('chefs/', views.about_chefs, name='about-chefs'),
]