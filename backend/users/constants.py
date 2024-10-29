from django.db.models import TextChoices


class SexChoice(TextChoices):
    """Выбор пола."""

    MALE = "male", "мужской"
    FEMALE = "female", "женский"


OTP_TOKEN_VALIDATION_TIME = 2
OTP_TOKEN_USE_TIME = 30
DEFAULT_OTP_TOKEN = 1234


class OTPTokenType(TextChoices):
    """Тип выдачи OTP токена."""

    LOGIN = "login", "Вход в личный кабинет"
    BOOKING = "booking", "Подтверждение бронирования"
    REQUEST = "request", "Заявка"


TOKEN_EXPIRED = "token_expired"
TOKEN_INVALID = "token_invalid"
