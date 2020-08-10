from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken

User = get_user_model()


class UserActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, callback, callback_args, callback_kwargs):
        if hasattr(request, "user") and request.user.is_authenticated:
            request.user.last_request = now()
            request.user.save(update_fields=["last_request"])

        return None


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
            result = authentication.JWTAuthentication().authenticate(request)
            request.user = result[0] if result else AnonymousUser()
        except InvalidToken:
            return self.get_response(request)
