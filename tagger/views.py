from rest_framework import generics
from django.contrib.auth import get_user_model

from tagger.serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer