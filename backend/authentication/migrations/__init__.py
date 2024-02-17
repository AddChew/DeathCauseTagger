import os


def create_default_user(apps, schema_editor):
    """
    Create default user if it does not exist.
    """
    User = apps.get_model("authentication.User")

    username = os.getenv("DEFAULT_USER", "admin")
    password = os.getenv("DEFAULT_PASSWORD", "admin")

    try:
        User.objects.get(username = username)
        
    except User.DoesNotExist:
        User.objects.create_superuser(username, password)