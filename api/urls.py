from django.urls import path
from .views import hello, BlogAPIView, AddBlogAPIView, UpdateDestroyAPIView

urlpatterns = [
    path('hello', hello, name='hello'),
    path('blog-list', BlogAPIView.as_view(), name='blog_list'),
    path('create-blog', AddBlogAPIView.as_view(), name='blog_create'),
    path('blog/<int:pk>', UpdateDestroyAPIView.as_view(), name='blog'),
]
