import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


def get_token(request):
    authorization = request.META.get('HTTP_AUTHORIZATION', "")
    if authorization:
        return authorization.split(" ")[-1]
    else:
        return None


def get_payload_user(request, token=None):
    data = {}

    if token is None:
        token = get_token(request)
    if token:
        try:
            data = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=['HS256'])
        except jwt.PyJWTError as e:
            raise PermissionDenied()

    return data


class CustomAuthentication(BaseAuthentication):
    token = None

    def get_user(self, request, response):
        username = response.get('username', None)
        user_model = get_user_model()
        user = user_model.objects.filter(email=username)
        if not user.exists():
            user = user_model.objects.filter(phone_number=username)
            if not user.exists():
                raise AuthenticationFailed(detail='Invalid payload')
        elif not user.first().is_confirmed:
            raise AuthenticationFailed(detail='User is not confirmed')
        return user.first()

    def authenticate(self, request, **kwargs):
        self.token = get_token(request)

        user = get_payload_user(request)

        if user:
            user_object = self.get_user(request, user)
            if user_object:
                return user_object, self.token

        return None, self.token
