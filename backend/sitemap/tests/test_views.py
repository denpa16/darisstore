import pytest
from django.urls import reverse
from rest_framework import status


class TestSitemapViews:
    """Тест Sitemap."""

    @pytest.mark.django_db
    def test_sitemap_view(self, api_client, django_assert_max_num_queries, set_site_id):
        """Тест view сайтмапа."""
        url = reverse("sitemap")
        with django_assert_max_num_queries(8):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
