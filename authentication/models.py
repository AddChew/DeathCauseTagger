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