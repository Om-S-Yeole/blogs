from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about_me, name='about-me'),
    path('contact-us/', views.contact_us, name='contact-us'),
]