from django.urls import path
from . import views
from .views import AddCommentView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about_me, name='about-me'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('posts/<str:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<str:slug>/comments/', views.LoadCommentsView.as_view(), name='load-comments'),
    path('posts/<str:slug>/like/', views.like_post, name='like-post'),
    path('posts/<str:slug>/comment/', AddCommentView.as_view(), name='add-comment'),
]