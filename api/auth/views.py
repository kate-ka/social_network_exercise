from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import UserSerializer, JWTObtainSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class JWTObtainView(TokenObtainPairView):
    serializer_class = JWTObtainSerializer
