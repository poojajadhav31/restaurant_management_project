from django.urls import path
from . import views

urlpatterns = [
   path('' ,views.homepage_view, name='home'), 
   path('about/', views.about_view, name = 'about'),
   path('menu/', menu_list_view, name='menu_list'),
   path('contact/' views.contact_view, name "contact")
   path('reservations/' views,reservations_view, name="reservations"),
]