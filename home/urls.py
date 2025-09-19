from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import MenuCategoryListView


urlpatterns = [
    path('', views.homepage_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('menu/', views.menu_view, name='menu_list'),
    path('api/menu-categories/', MenuCategoryListView.as_view(), name='menu-categories'),
    path('contact/', views.contact_view, name="contact"),
    path('contact/success/', views.contact_success, name="contact_success"),  
    path('reservations/', views.reservations_view, name="reservations"),
    path('feedback/', views.feedback_view, name='feedback'),
    path('faq/', views.faq_view, name="faq"),

    # auth routes
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="home/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),
]
