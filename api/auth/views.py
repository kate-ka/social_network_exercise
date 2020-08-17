from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import (
    UserSerializer,
    JWTObtainSerializer,
    UserActivitySerializer,
)

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class JWTObtainView(TokenObtainPairView):
    serializer_class = JWTObtainSerializer


class UserActivityViewSet(
    viewsets.mixins.RetrieveModelMixin,
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    lookup_field = "username"
    lookup_value_regex = "[^@]+@[^@]+\.[^@]+"
