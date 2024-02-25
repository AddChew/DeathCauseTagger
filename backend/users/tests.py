import os
import pytest

from users.models import User


username = "test"
credentials = {
    "username": username,
    "password": username,
}
register_endpoint = "/api/v1/token/register"


@pytest.mark.django_db
class TestUsers:

    def test_register_user_success(self, client):
        response = client.post(
            register_endpoint,
            credentials,
            content_type = "application/json",
        )
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["username"] == username
        assert isinstance(json_response["refresh"], str)
        assert isinstance(json_response["access"], str)

        assert User.objects.filter(username = username).exists()

    def test_register_user_missing_username_password(self, client):
        response = client.post(
            register_endpoint,
            {},
            content_type = "application/json",
        )
        assert response.status_code == 400

        json_response = response.json()
        assert json_response == {
            "detail": "Invalid input.",
            "code": "invalid",
            "username": "username is required",
            "password": "password is required"
        }

    def test_register_user_missing_username(self, client):
        data = {
            "password": username,
        }
        response = client.post(
            register_endpoint,
            data,
            content_type = "application/json",
        )
        assert response.status_code == 400

        json_response = response.json()
        assert json_response == {
            "detail": "Invalid input.",
            "code": "invalid",
            "username": "username is required"
        }

    def test_register_user_missing_password(self, client):
        data = {
            "username": username,
        }
        response = client.post(
            register_endpoint,
            data,
            content_type = "application/json",
        )
        assert response.status_code == 400

        json_response = response.json()
        assert json_response == {
            "detail": "Invalid input.",
            "code": "invalid",
            "password": "password is required"
        }

    def test_register_user_already_exists(self, client):
        data = {
            "username": os.getenv("DEFAULT_USER", "admin"),
            "password": os.getenv("DEFAULT_PASSWORD", "admin")
        }
        response = client.post(
            register_endpoint,
            data,
            content_type = "application/json",
        )
        assert response.status_code == 409

        json_response = response.json()
        assert json_response == {
            "detail": "Username already exists",
            "code": "register_fail"
        }

    def test_create_superuser_success(self):
        User.objects.create_superuser(**credentials)
        superuser = User.objects.get(username = username)

        assert superuser.is_active
        assert superuser.is_staff
        assert superuser.is_superuser

    def test_create_superuser_failure_is_staff(self):
        with pytest.raises(ValueError, match = "Superuser must have is_staff=True."):
            User.objects.create_superuser(**credentials, **{"is_staff": False})

    def test_create_superuser_failure_is_superuser(self):
        with pytest.raises(ValueError, match = "Superuser must have is_superuser=True."):
            User.objects.create_superuser(**credentials, **{"is_superuser": False})

    def test_get_default_user(self):
        default_username = os.getenv("DEFAULT_USER", "admin")
        default_user = User.objects.get(username = default_username)
        assert User.get_default_user() == default_user.id