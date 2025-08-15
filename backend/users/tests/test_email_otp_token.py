import pytest
from django.urls import reverse
from rest_framework import status

from users.constants import DEFAULT_OTP_TOKEN
from users.models import EmailOTPToken
from users.tests.factories import EmailOTPTokenFactory


class TestEmailOTPViewSet:
    """Тесты email OTP-токенов."""

    @pytest.mark.django_db()
    def test_create_email_otp_token(self, api_client, django_assert_max_num_queries):
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
        assert db_otp_token.otp == DEFAULT_OTP_TOKEN

    @pytest.mark.django_db()
    def test_validate_email_otp_token(self, api_client, django_assert_max_num_queries):
        """Тест подтверждения email OTP-токена."""
        url = reverse("email_otp_token-validate_otp_token")
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
