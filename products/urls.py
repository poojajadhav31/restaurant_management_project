from django.urls import path
from .views import menu_api
from . import views

urlpatterns = [
    path('menu/', menu_api, name='menu-api'),
    path('specials/', views.todays_specials, name='todays-specials'),
    path('chefs/', views.about_chefs, name='about-chefs'),
]