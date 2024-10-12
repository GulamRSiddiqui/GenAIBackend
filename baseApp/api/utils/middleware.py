# myapp/middleware.py

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed

class JWTMiddleware(MiddlewareMixin):
    def process_request(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            try:
                token = token.split(" ")[1]  # Get the token part after "Bearer"
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = User.objects.get(id=payload['user_id'])  # Use your payload key
                request.user = user
            except (jwt.ExpiredSignatureError, jwt.DecodeError, User.DoesNotExist):
                request.user = None  # Or handle accordingly
                raise AuthenticationFailed('Invalid token')
