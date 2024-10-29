import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User
from users.tests.factories import UserFactory, OTPTokenFactory, EmailOTPTokenFactory
from users.constants import DEFAULT_OTP_TOKEN


class TestUserViewSet:
    """Тесты API пользователя."""

    @pytest.mark.django_db()
    def test_logout(self, api_client, django_assert_max_num_queries):
        """Тест логаута."""
        user = UserFactory()
        api_client.force_login(user)
        url = reverse("users-logout")
        with django_assert_max_num_queries(1):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_list(self, api_client, django_assert_max_num_queries):
        """Тест метода списка."""
        user = UserFactory()
        api_client.force_login(user)
        url = reverse("users-list")
        with django_assert_max_num_queries(1):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()["data"]
        assert res_json["id"] == user.id
        assert res_json["username"] == user.username

    @pytest.mark.django_db()
    def test_retrieve(self, api_client, django_assert_max_num_queries):
        """Тест детального просмотра."""
        user = UserFactory()
        api_client.force_login(user)
        url = reverse("users-detail", kwargs={"pk": user.id})
        with django_assert_max_num_queries(1):
            response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()["data"]
        assert res_json["id"] == user.id
        assert res_json["username"] == user.username

    @pytest.mark.django_db()
    def test_register_phone_action(self, api_client, django_assert_max_num_queries):
        """Тест регистрации по номеру телефона."""
        phone = "+79999993456"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN, used=True)
        data = {
            "phone": phone,
            "uid": db_otp_token.uid,
            "otp": db_otp_token.otp,
            "first_name": 1,
            "last_name": "Last",
            "patronymic": "Patronymic",
            "email": "test@test.ru"
        }
        url = reverse("users-phone_register")
        with django_assert_max_num_queries(6):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED
        res_json = response.json()["data"]
        db_user = User.objects.first()
        assert res_json["id"] == db_user.pk
        assert res_json["username"] == db_user.username
        assert res_json["phone"] == db_user.phone

    @pytest.mark.django_db()
    def test_error_register_phone_action(self, api_client, django_assert_max_num_queries):
        """Тест регистрации с ошибкой по номеру телефона."""
        phone = "+79999993456"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN)
        UserFactory(phone=phone)
        data = {
            "phone": phone,
            "uid": db_otp_token.uid,
            "otp": db_otp_token.otp
        }
        url = reverse("users-phone_register")
        with django_assert_max_num_queries(5):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        db_users = User.objects.all()
        assert len(db_users) == 1

    @pytest.mark.django_db()
    def test_phone_login_action(self, api_client, django_assert_max_num_queries):
        """Тест логина по телефону."""
        phone = "+79999993456"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN, used=True)
        UserFactory(phone=phone)
        data = {
            "phone": phone,
            "uid": db_otp_token.uid,
            "otp": db_otp_token.otp
        }
        url = reverse("users-phone_login")
        with django_assert_max_num_queries(5):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_without_existed_phone_login_action(self, api_client, django_assert_max_num_queries):
        """Тест логина по телефону без существующего пользователя."""
        phone = "+79064445678"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN, used=True)
        data = {
            "phone": phone,
            "uid": db_otp_token.uid,
            "otp": db_otp_token.otp
        }
        url = reverse("users-phone_login")
        with django_assert_max_num_queries(4):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db()
    def test_error_phone_login_action(self, api_client, django_assert_max_num_queries):
        """Тест логина по телефону с непотвержденным токеном."""
        phone = "+79064445678"
        db_otp_token = OTPTokenFactory(phone=phone, otp=DEFAULT_OTP_TOKEN)
        UserFactory(phone=phone)
        data = {
            "phone": phone,
            "uid": db_otp_token.uid,
            "otp": db_otp_token.otp
        }
        url = reverse("users-phone_login")
        with django_assert_max_num_queries(4):
            response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
