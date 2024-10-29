import pytest
from django.urls import reverse
from rest_framework import status

from users.constants import DEFAULT_OTP_TOKEN, OTPTokenType
from users.models import OTPToken
from users.tests.factories import OTPTokenFactory


class TestOTPViewSet:
    """Тесты OTP-токенов."""

    @pytest.mark.django_db
    def test_create_otp_token(self, api_client, django_assert_max_num_queries):
        """Тест создания OTP-токена."""
        url = reverse("otp_token-list")
        data = {"phone": "+79991234567", "type": OTPTokenType.LOGIN}
        with django_assert_max_num_queries(2):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        otp_tokens = OTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.phone == data["phone"]
        assert db_otp_token.otp == str(DEFAULT_OTP_TOKEN)

    @pytest.mark.django_db
    def test_validate_action(self, api_client, django_assert_max_num_queries):
        """Тест подтверждения OTP-токена."""
        url = reverse("otp_token-validate")
        phone = "+79993455667"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN)
        data = {
            "phone": phone,
            "otp": DEFAULT_OTP_TOKEN,
            "uid": db_otp_token.uid,
        }
        with django_assert_max_num_queries(3):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK
        otp_tokens = OTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.used is True

    @pytest.mark.django_db
    def test_error_create_action(self, api_client, django_assert_max_num_queries):
        """Тест создания с ошибкой OTP-токена."""
        url = reverse("otp_token-list")
        data = {"phone": "+79991234567", "type": OTPTokenType.LOGIN}
        with django_assert_max_num_queries(2):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        otp_tokens = OTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.phone == data["phone"]
        assert db_otp_token.otp == str(DEFAULT_OTP_TOKEN)
        attempt_counts = 15
        [OTPTokenFactory(phone=data["phone"]) for _ in range(attempt_counts)]
        with django_assert_max_num_queries(2):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_error_validate_action(self, api_client, django_assert_max_num_queries):
        """Тест подтверждения с ошибкой OTP-токена."""
        url = reverse("otp_token-validate")
        phone = "+79993455667"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN)
        error_code = 1256
        data = {
            "phone": phone,
            "otp": error_code,
            "uid": db_otp_token.uid,
        }
        with django_assert_max_num_queries(3):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        otp_tokens = OTPToken.objects.all()
        assert len(otp_tokens) == 1
        db_otp_token = otp_tokens[0]
        assert db_otp_token.used is False
