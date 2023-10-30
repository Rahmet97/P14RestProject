from django.urls import path

from .views import OneIDAuthAPIView, OneIDCodeAPIView

urlpatterns = [
    path('login', OneIDAuthAPIView.as_view(), name='oneid_login'),
    path('code', OneIDCodeAPIView.as_view(), name='oneid_code'),
]
