from django.urls import path
from . import views

urlpatterns = [
   path('' ,views.homepage_view, name='home'), 
   path('about/', views.about_view, name = 'about'),
   path('menu/', menu_view, name='menu_list'),
   path('contact/' views.contact_view, name "contact"),
   path('contact/success/', views.contact_success, name="contact_success")
   path('reservations/' views,reservations_view, name="reservations"),
   path('feedback/',feedback_view, name='feedback'),
   path('faq/' , faq_view, name="faq"),
   path("login/", auth_views.LoginView.auth_view(template_name="home/login.html"), name="login",),
   path("logout/",auth_views.LogoutView.as_view(next_page="homepage"), name="logout"),
]