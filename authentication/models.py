import os
from authentication.managers import UserManager
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
        Custom User Model
    """
    first_name = None
    last_name = None
    email = None

    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.username

    @classmethod
    def get_default_user(cls):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'superuser')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'password')

        try:
            default_user = cls.objects.get(username = username)

        except cls.DoesNotExist:
            default_user = cls.objects.create_superuser(username, password)

        return default_user.id