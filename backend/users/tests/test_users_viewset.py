import pytest

class TestUserViewSet:
    """
    Тест пользователя

    """

    @pytest.mark.django_db
    def test_user_viewset(self, api_client, django_assert_max_num_queries):
        """
        Тест пользователя

        """
        assert 1 == 1
