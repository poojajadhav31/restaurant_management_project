from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import menu_api, ProductUpdateViewSet, todays_specials, about_chefs

router = DefaultRouter()
router.register(r'update', ProductUpdateViewSet, basename='product-update')

urlpatterns = [
    path('menu/', menu_api, name='menu-api'),
  
    path('specials/', todays_specials, name='todays-specials'),
    path('chefs/', about_chefs, name='about-chefs'),
]

urlpatterns += router.urls