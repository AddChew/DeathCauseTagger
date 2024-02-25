import os
import pytest

from users.models import User


register_endpoint = "/api/v1/token/register"


@pytest.mark.django_db
class TestUsers:

    def test_register_user_success(self, client):
        username = "test"
        data = {
            "username": username,
            "password": username,
        }
        response = client.post(
            register_endpoint,
            data,
            content_type = "application/json",
        )
        assert response.status_code == 200

        json_response = response.json()
        assert json_response["username"] == username
        assert isinstance(json_response["refresh"], str)
        assert isinstance(json_response["access"], str)

        assert User.objects.filter(username = username).exists()

    def test_register_user_missing_username_password(self, client):
        data = {}
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
            "username": "username is required",
            "password": "password is required"
        }

    def test_register_user_missing_username(self, client):
        data = {
            "password": "test"
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
            "username": "test"
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