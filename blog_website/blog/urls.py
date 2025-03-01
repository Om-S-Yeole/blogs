from django.urls import path
from . import views
from .views import AddCommentView, PostCreateView, CategoryCreateView, PostUpdateView, PostDeleteView, CommentDeleteView
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about_me, name='about-me'),
    path('contact-us/', views.contact_us, name='contact-us'),
    path('terms-and-conditions/', TemplateView.as_view(template_name='blog/terms_and_conditions.html'), name='terms-and-conditions'),
    path('privacy-policy/', TemplateView.as_view(template_name='blog/privacy_policy.html'), name='privacy-policy'),
    path('posts/<str:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<str:slug>/comments/', views.LoadCommentsView.as_view(), name='load-comments'),
    path('posts/<str:slug>/like/', views.like_post, name='like-post'),
    path('posts/<str:slug>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('posts/create/new-category', CategoryCreateView.as_view(), name='new-category'),
    path('posts/create/new-post', PostCreateView.as_view(), name='new-post'),
    path('posts/<str:slug>/update/', PostUpdateView.as_view(), name='update-post'),
    path('posts/<str:slug>/delete/', PostDeleteView.as_view(), name='delete-post'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='delete-comment'),
]