from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers import UserSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer