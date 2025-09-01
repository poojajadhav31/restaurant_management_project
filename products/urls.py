from django.urls import path
from .views import menu_api

urlpatterns = [
    path('menu/', menu_api, name='menu-api'),
    # path('specials/', todays_specials, name='todays-specials'),
]