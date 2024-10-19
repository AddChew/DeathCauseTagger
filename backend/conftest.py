import os
import pytest


@pytest.fixture
def access_token(client):
    token_endpoint = "/api/v1/token/pair"
    data = {
        "username": os.getenv("DEFAULT_USER", "admin"),
        "password": os.getenv("DEFAULT_PASSWORD", "admin")
    }
    response = client.post(token_endpoint, data, content_type = "application/json")
    json_response = response.json()
    return json_response["access"]
