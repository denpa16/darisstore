from uuid import uuid4

from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from common.tasks import send_sms
from common.utils import generate_code
from users.backends.send_mail import send_mail

from ..constants import OTPTokenType

SMS_MESSAGE_TEMPLATE = "%s код для входа в Личный кабинет"
SMS_BOOKING_MESSAGE_TEMPLATE = "%s код для подтверждения бронирования"
DEFAULT_OTP_TOKEN = "1234"


class OTPToken(models.Model):
    """Модель для хранения СМС-токенов"""

    created = models.DateTimeField("Создано", default=timezone.now)
    phone = PhoneNumberField("Номер", db_index=True)
    otp = models.CharField("Код", max_length=8, db_index=True)
    used = models.BooleanField("Подтверждённый", default=False)
    uid = models.UUIDField("UID", db_index=True, default=uuid4)

    class Meta:
        ordering = ("created",)
        verbose_name = "OTP-токен"
        verbose_name_plural = "OTP-токены"

    def __str__(self):
        return f"{self.phone} - {self.otp}"

    @classmethod
    def create(cls, phone_number, token_type=OTPTokenType.LOGIN):
        otp = cls.generate_otp(4)
        token = cls._default_manager.create(phone=phone_number, otp=otp)
        phone = str(phone_number)
        if phone.startswith("+"):
            phone = phone[1:]
        if not settings.SMS_DEBUG:
            if token_type == OTPTokenType.BOOKING:
                message = SMS_BOOKING_MESSAGE_TEMPLATE % otp
            else:
                message = SMS_MESSAGE_TEMPLATE % otp
            send_sms(to=phone, body=message)
        return token

    @classmethod
    def generate_otp(cls, length=4):
        return generate_code(length) if not settings.SMS_DEBUG else DEFAULT_OTP_TOKEN


class EmailOTPToken(models.Model):
    created = models.DateTimeField("Создано", default=timezone.now)
    email = models.EmailField("Email", db_index=True)
    otp = models.CharField("Код", max_length=8, db_index=True)
    used = models.BooleanField("Подтверждённый", default=False)
    uid = models.UUIDField("UID", db_index=True, default=uuid4)

    class Meta:
        ordering = ("created",)
        verbose_name = "Email OTP-токен"
        verbose_name_plural = "Email OTP-токены"

    def __str__(self):
        return f"{self.email} - {self.otp}"

    @classmethod
    def create(cls, email):
        otp = cls.generate_otp(4)
        token = cls._default_manager.create(email=email, otp=otp)
        message = f"Код подтверждния: {otp}"
        subject = "Код подтверждения"
        send_mail(subject=subject, message=message, email=email)
        return token

    @classmethod
    def generate_otp(cls, length=4):
        return generate_code(length)
