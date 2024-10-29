import pytest
from django.urls import reverse
from rest_framework import status

from users.constants import DEFAULT_OTP_TOKEN
from users.models import EmailOTPToken
from users.tests.factories import EmailOTPTokenFactory


class TestEmailOTPViewSet:
    """Тесты email OTP-токенов."""

    @pytest.mark.django_db
    def test_create_action(self, api_client, django_assert_max_num_queries):
        """Тест создания email OTP-токена."""
        url = reverse("email_otp_token-list")
        data = {"email": "admin@admin.com"}
        with django_assert_max_num_queries(2):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        otp_tokens = EmailOTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.email == data["email"]
        assert db_otp_token.otp == str(DEFAULT_OTP_TOKEN)

    @pytest.mark.django_db
    def test_validate_action(self, api_client, django_assert_max_num_queries):
        """Тест подтверждения email OTP-токена."""
        url = reverse("email_otp_token-validate")
        email = "admin@admin.com"
        db_otp_token = EmailOTPTokenFactory(email=email, otp=DEFAULT_OTP_TOKEN)
        data = {
            "email": email,
            "otp": DEFAULT_OTP_TOKEN,
            "uid": db_otp_token.uid,
        }
        with django_assert_max_num_queries(3):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        otp_tokens = EmailOTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.used is True

    @pytest.mark.django_db
    def test_error_create_action(self, api_client, django_assert_max_num_queries):
        """Тест создания с ошибкой email OTP-токена."""
        url = reverse("email_otp_token-list")
        data = {"email": "test@test.com"}
        with django_assert_max_num_queries(2):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        otp_tokens = EmailOTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.email == data["email"]
        assert db_otp_token.otp == str(DEFAULT_OTP_TOKEN)
        attempt_counts = 15
        [EmailOTPTokenFactory(email=data["email"]) for _ in range(attempt_counts)]
        with django_assert_max_num_queries(2):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_error_validate(self, api_client, django_assert_max_num_queries):
        """Тест подтверждения с ошибкой email OTP-токена."""
        url = reverse("email_otp_token-validate")
        email = "admin@admin.com"
        db_otp_token = EmailOTPTokenFactory(email=email, otp=DEFAULT_OTP_TOKEN)
        error_code = 1256
        data = {
            "email": email,
            "otp": error_code,
            "uid": db_otp_token.uid,
        }
        with django_assert_max_num_queries(3):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        otp_tokens = EmailOTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.used is False
