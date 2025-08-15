import pytest


@pytest.fixture()
def api_client():
    """Вспомогательный метод для тестов."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture()
def api_client_auth():
    """Вспомогательный метод для тестов с использованием авторизации."""
    from rest_framework.test import APIClient

    from users.tests.factories import UserFactory

    user = UserFactory()
    client = APIClient()
    client.force_login(user)
    return client
