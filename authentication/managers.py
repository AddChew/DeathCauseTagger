from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username: str, password: str, **extra_fields):
        if not username:
            raise ValueError(_('The Username must be set'))
        user = self.model(username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)