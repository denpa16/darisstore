import factory
from django.contrib.auth import get_user_model

from users.constants import DEFAULT_OTP_TOKEN
from users.models import EmailOTPToken, OTPToken

User = get_user_model()


class OTPTokenFactory(factory.django.DjangoModelFactory):
    """Фабрика otp-токена."""

    otp = DEFAULT_OTP_TOKEN

    class Meta:
        model = OTPToken


class EmailOTPTokenFactory(factory.django.DjangoModelFactory):
    """Фабрика emailotp-токена."""

    otp = DEFAULT_OTP_TOKEN

    class Meta:
        model = EmailOTPToken


class UserFactory(factory.django.DjangoModelFactory):
    """Фабрика пользователя."""

    username = factory.Sequence(lambda number: f"user_{number}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")

    class Meta:
        model = User
