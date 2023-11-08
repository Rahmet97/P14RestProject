import os

import requests
from allauth.socialaccount.models import SocialApp
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.views import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from accounts.serializers import UserSerializer

User = get_user_model()


class RegisterAPIView(APIView):

    def post(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        username = request.data.get('username')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'message': 'This email already exists!'}, status=400)
            if User.objects.filter(username=username).exists():
                return Response({'success': False, 'message': 'This username already exists!'}, status=400)
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password1
                )
                return Response({'success': True, 'message': 'Successfully registered'})
        else:
            return Response({'success': False, 'message': 'Passwords are not same!'}, status=400)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=204)


class UserInfoAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)


class RedirectToGoogleAPIView(APIView):

    def get(self, request):
        google_redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')
        try:
            google_client_id = SocialApp.objects.get(provider='google').client_id
        except SocialApp.DoesNotExist:
            return Response({'success': False, 'message': 'SocialApp does not exist'}, status=404)
        url = f'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={google_redirect_uri}&prompt=consent&response_type=code&client_id={google_client_id}&scope=openid email profile&access_type=offline'
        return redirect(url)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = 'https://75f8-185-139-138-214.ngrok-free.app/accounts/google/callback'
    client_class = OAuth2Client


class GithubLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GitHubOAuth2Adapter
    callback_url = 'https://75f8-185-139-138-214.ngrok-free.app/accounts/github/callback'
    client_class = OAuth2Client


@api_view(["GET"])
def callback(request):
    """Callback"""
    code = request.GET.get("code")

    # exchange code with authorization server for access token and ID token
    res = requests.post("http://localhost:8000/accounts/google", data={"code": code}, timeout=30)
    print('Response >>>', res.json())

    # return ID token to the user which will be used by the user in subsequent requests to verify his identity
    return Response(res.json())


@api_view(["GET"])
def callback_github(request):
    """Callback"""
    code = request.GET.get("code")

    # exchange code with authorization server for access token and ID token
    res = requests.post("http://localhost:8000/accounts/github", data={"code": code}, timeout=30)
    print('Response >>>', res.json())

    # return ID token to the user which will be used by the user in subsequent requests to verify his identity
    return Response(res.json())
