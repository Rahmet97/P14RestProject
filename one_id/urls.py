from django.urls import path

from .views import OneIDAuthAPIView, OneIDCodeAPIView, OneIDLogoutAPIView

urlpatterns = [
    path('login', OneIDAuthAPIView.as_view(), name='oneid_login'),
    path('logout', OneIDLogoutAPIView.as_view(), name='oneid_logout'),
    path('code', OneIDCodeAPIView.as_view(), name='oneid_code'),
]
