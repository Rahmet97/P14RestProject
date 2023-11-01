import os
import requests

from django.shortcuts import redirect
from django.contrib.auth.views import get_user_model
from dotenv import load_dotenv
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from one_id.models import OneIDProfile, OneIDLegalInfo

load_dotenv()
BASE_URL = 'https://sso.egov.uz/sso/oauth/Authorization.do'
User = get_user_model()


class OneIDAuthAPIView(GenericAPIView):
    permission_classes = ()

    def get(self, request):
        response_type = 'one_code'
        client_id = os.getenv('CLIENT_ID')
        redirect_uri = 'http://127.0.0.1:8000/oneid/code'
        scope = 'testScope'
        state = 'testState'

        return redirect(f'{BASE_URL}?response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&Scope={scope}&state={state}')


class OneIDCodeAPIView(GenericAPIView):
    permission_classes = ()

    def get_access_token(self):
        code = self.request.GET.get('code')
        grant_type = 'one_authorization_code'
        client_id = os.getenv('CLIENT_ID')
        secret_key = os.getenv('SECRET_KEY')
        redirect_uri = 'http://127.0.0.1:8000/oneid/code'

        response = requests.post(BASE_URL, params={
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': secret_key,
            'redirect_uri': redirect_uri,
            'code': code
        })

        return response.json()

    def get_info(self, access_token):
        grant_type = 'one_access_token_identify'
        client_id = os.getenv('CLIENT_ID')
        secret_key = os.getenv('SECRET_KEY')
        scope = 'testScope'

        response = requests.post(BASE_URL, params={
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': secret_key,
            'access_token': access_token,
            'scope': scope
        })
        return response.json()

    def create_or_update_profile(self, one_id_profile):
        if one_id_profile['legal_info']:
            password = one_id_profile['le_name'][2] + one_id_profile['tin'] + one_id_profile['le_name'][-1]
        else:
            password = one_id_profile['first_name'][0] + one_id_profile['pin'] + one_id_profile['first_name'][-1]
        if User.objects.filter(username=one_id_profile['user_id']).exists():
            user = User.objects.get(username=one_id_profile['user_id'])
        else:
            user = User.objects.create_user(
                username=one_id_profile['user_id'],
                password=password
            )
        data = {
            'user': user,
            'birth_date': one_id_profile['birth_date'],
            'ctzn': one_id_profile['ctzn'],
            'per_adr': one_id_profile['per_adr'],
            'pport_issue_place': one_id_profile['pport_issue_place'],
            'sur_name': one_id_profile['sur_name'],
            'gd': one_id_profile['gd'],
            'natn': one_id_profile['natn'],
            'pport_issue_date': one_id_profile['pport_issue_date'],
            'pport_expr_date': one_id_profile['pport_expr_date'],
            'pport_no': one_id_profile['pport_no'],
            'pin': one_id_profile['pin'],
            'mob_phone_no': one_id_profile['mob_phone_no'],
            'username': one_id_profile['user_id'],
            'email': one_id_profile['email'],
            'birth_place': one_id_profile['birth_place'],
            'mid_name': one_id_profile['mid_name'],
            'user_type': one_id_profile['user_type'],
            'sess_id': one_id_profile['sess_id'],
            'ret_cd': one_id_profile['ret_cd'],
            'first_name': one_id_profile['first_name'],
            'full_name': one_id_profile['full_name'],
            'valid': True if one_id_profile['valid'] == 'true' else False
        }
        if OneIDProfile.objects.filter(mob_phone_no=one_id_profile['mob_phone_no']).exists():
            one_id_user = OneIDProfile.objects.filter(mob_phone_no=one_id_profile['mob_phone_no'])
            one_id_user.update(**data)
            one_id_user = one_id_user.first()
        else:
            one_id_user = OneIDProfile.objects.create(**data)
        one_id_user.save()

        return one_id_user

    def create_or_update_legal_info(self, one_id_profile, one_id_user):
        if one_id_profile['legal_info']:
            data = {
                'profile': one_id_user,
                'le_tin': one_id_profile['legal_info']['le_tin'],
                'tin': one_id_profile['legal_info']['tin'],
                'legal_name': one_id_profile['legal_info']['le_name'],
                'acron_uz': one_id_profile['legal_info']['acron_UZ'],
                'is_basic': True if one_id_profile['legal_info']['is_basic'] == 'true' else False
            }
            if OneIDLegalInfo.objects.filter(tin=one_id_profile['legal_info']['tin']).exists():
                legal_info = OneIDLegalInfo.objects.filter(tin=one_id_profile['legal_info']['tin'])
                legal_info.update(**data)
                legal_info = legal_info.first()
            else:
                legal_info = OneIDLegalInfo.objects.create(**data)
            legal_info.save()

    def get(self, request):
        try:
            token = self.get_access_token()
            access_tk = token['access_token']
            one_id_profile_data = self.get_info(access_tk)
            one_id_profile = self.create_or_update_profile(one_id_profile_data)
            tk = RefreshToken.for_user(one_id_profile.user)
            tokens = {
                'access_token': str(tk.access_token),
                'refresh_token': str(tk),
                'one_id_access_token': access_tk
            }
            self.create_or_update_legal_info(one_id_profile_data, one_id_profile)
        except Exception as e:
            return Response({'success': False, 'message': e})
        return Response(tokens)


class OneIDLogoutAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        grant_type = 'one_log_out'
        client_id = os.getenv('CLIENT_ID')
        secret_key = os.getenv('SECRET_KEY')
        scope = 'testScope'

        response = requests.post(BASE_URL, params={
            'grant_type': grant_type,
            'client_id': client_id,
            'client_secret': secret_key,
            'access_token': request.META.get('HTTP_ONEID_TOKEN'),
            'scope': scope
        })
        return Response(status=204)
