import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def get_auth_client(client: APIClient, user) -> APIClient:
    client.force_authenticate(user)
    return client
