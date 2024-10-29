import os
import shutil

import pytest
from django.conf import settings
from django.contrib.sites.models import Site


@pytest.fixture
def api_client():
    """Вспомогательный метод для тестов."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def api_client_auth():
    """Вспомогательный метод для тестов с использованием авторизации."""
    from rest_framework.test import APIClient

    from users.tests.factories import UserFactory

    user = UserFactory()
    client = APIClient()
    client.force_login(user)
    return client


@pytest.fixture(scope="session", autouse=True)
def _clear_media_files() -> None:
    """Метод для удаления медиа после завершения тестов."""
    if os.path.exists(settings.MEDIA_ROOT):
        shutil.rmtree(settings.MEDIA_ROOT)
    os.makedirs(settings.MEDIA_ROOT)

    yield

    # Cleanup after tests are done
    if os.path.exists(settings.MEDIA_ROOT):
        shutil.rmtree(settings.MEDIA_ROOT)


@pytest.fixture
def example_site(db):
    """Fixture для Site."""
    return Site.objects.create(domain="test_example.com", name="test_example")


@pytest.fixture
def set_site_id(example_site, settings) -> int:
    """Установка SITE ID для теста sitemap."""
    settings.SITE_ID = example_site.id
    return settings.SITE_ID
