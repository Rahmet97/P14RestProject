from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenBlacklistView,
)

from .views import RegisterAPIView, UserInfoAPIView, LogoutAPIView, FacebookLogin, GoogleLogin, callback, \
    callback_github, GithubLogin, RedirectToGoogleAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('user-info', UserInfoAPIView.as_view(), name='user_info'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('facebook', FacebookLogin.as_view(), name='fb_login'),
    path('google', GoogleLogin.as_view(), name='google_login'),
    path('google-login', RedirectToGoogleAPIView.as_view(), name='google_login2'),
    path('github', GithubLogin.as_view(), name='github_login'),
    path('google/callback', callback, name='google_callback'),
    path('github/callback', callback_github, name='github_callback')
]
