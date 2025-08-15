from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from common.tasks import send_sms
from common.utils import generate_code
from users.backends.send_mail import send_mail
from users.constants import DEFAULT_OTP_TOKEN, OTPTokenType

SMS_MESSAGE_TEMPLATE = "%s код для входа в Личный кабинет"
SMS_BOOKING_MESSAGE_TEMPLATE = "%s код для подтверждения бронирования"
SMS_REQUEST_MESSAGE_TEMPLATE = "%s код для подтверждения заявки"


class OTPToken(models.Model):
    """Модель для хранения СМС-токенов по номеру телефона."""

    created = models.DateTimeField(verbose_name="Создано", default=timezone.now)
    phone = PhoneNumberField(verbose_name="Номер", db_index=True)
    otp = models.CharField(verbose_name="Код", max_length=8, db_index=True)
    used = models.BooleanField(verbose_name="Подтверждённый", default=False)
    uid = models.UUIDField(verbose_name="UID", db_index=True, default=uuid4)

    class Meta:
        ordering = ("created",)
        verbose_name = "OTP-токен"
        verbose_name_plural = "OTP-токены"

    def __str__(self) -> str:
        return f"{self.phone} - {self.otp}"

    @classmethod
    def create(cls, phone_number, token_type=OTPTokenType.LOGIN) -> models.Model:
        """Создание одноразового кода."""
        otp = cls.generate_otp()
        token = cls._default_manager.create(phone=phone_number, otp=otp)
        phone = str(phone_number)
        if phone.startswith("+"):
            phone = phone[1:]
        if not settings.TESTING:
            if token_type == OTPTokenType.BOOKING:
                message = SMS_BOOKING_MESSAGE_TEMPLATE % otp
            elif token_type == OTPTokenType.REQUEST:
                message = SMS_REQUEST_MESSAGE_TEMPLATE % otp
            else:
                message = SMS_MESSAGE_TEMPLATE % otp
            send_sms.delay(phone, message)
        return token

    @classmethod
    def generate_otp(cls, length: int = 4) -> str:
        """Генерация кода."""
        #if not settings.TESTING:
        #    return generate_code(length)
        return DEFAULT_OTP_TOKEN


class EmailOTPToken(models.Model):
    """Модель для хранения СМС-токенов по email."""

    created = models.DateTimeField(verbose_name="Создано", default=timezone.now)
    email = models.EmailField(verbose_name="Email", db_index=True)
    otp = models.CharField(verbose_name="Код", max_length=8, db_index=True)
    used = models.BooleanField(verbose_name="Подтверждённый", default=False)
    uid = models.UUIDField(verbose_name="UID", db_index=True, default=uuid4)

    class Meta:
        ordering = ("created",)
        verbose_name = "Email OTP-токен"
        verbose_name_plural = "Email OTP-токены"

    def __str__(self) -> str:
        return f"{self.email} - {self.otp}"

    @classmethod
    def create(cls, email: str) -> models.Model:
        """Создание одноразового кода."""
        otp = cls.generate_otp(4)
        token = cls._default_manager.create(email=email, otp=otp)
        message = f"Код подтверждния: {otp}"
        subject = "Код подтверждения"
        if not settings.TESTING:
            send_mail(subject=subject, message=message, email=email)
        return token

    @classmethod
    def generate_otp(cls, length: int = 4) -> str:
        """Генерация кода."""
        if not settings.TESTING:
            return generate_code(length)
        return DEFAULT_OTP_TOKEN
