from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import hello, SubscriberAPIView, BlogViewSet, SearchDocumentViewSet, BlogFilterAPIView

routers = DefaultRouter()
routers.register('blog', BlogViewSet, basename='blog')
routers.register('search', SearchDocumentViewSet, basename='search')

urlpatterns = [
    path('hello', hello, name='hello'),
    # path('blog-list', BlogAPIView.as_view(), name='blog_list'),
    # path('create-blog', AddBlogAPIView.as_view(), name='blog_create'),
    # path('blog/<int:pk>', UpdateDestroyAPIView.as_view(), name='blog'),
    path('subscribe', SubscriberAPIView.as_view(), name='subscribe'),
    # path('search', SearchAPIView.as_view(), name='search'),
    path('filter', BlogFilterAPIView.as_view(), name='filter'),
    path('', include(routers.urls)),
]
