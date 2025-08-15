from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.indexes import GinIndex, OpClass
from django.core import validators
from django.db import models
from django.db.models.functions import Upper
from django.utils.crypto import salted_hmac
from phonenumber_field.modelfields import PhoneNumberField

from ..constants import SexChoice
from .managers import UserManager


class UserQuerySet(UserManager):
    """
    Менеджер пользователя
    """


class User(AbstractUser):
    """
    Пользователь
    """

    objects: UserQuerySet = UserQuerySet()

    avatar = models.ImageField(
        verbose_name="Аватар", upload_to="account/images/", blank=True, null=True
    )
    patronymic = models.CharField("Отчество", max_length=200, blank=True)
    email = models.CharField(
        verbose_name="Email",
        validators=[validators.validate_email],
        max_length=200,
        default=None,
        blank=True,
        null=True,
    )
    phone = PhoneNumberField(
        verbose_name="Номер телефона",
        blank=True,
        null=True,
    )
    resident = models.CharField("Резедент страны", max_length=200, blank=True, default="РФ")
    passport_number = models.CharField("Номер паспорта", max_length=30, blank=True)
    passport_serial = models.CharField("Серия паспорта", max_length=30, blank=True)
    birth_date = models.DateField("Дата рождения", default="1900-01-01", blank=True)
    gender = models.CharField("Пол", max_length=30, blank=True, choices=SexChoice.choices)
    phone_additional = PhoneNumberField(
        "Дополнительный номер телефона",
        blank=True,
        null=True,
    )

    stop_sending_sms = models.BooleanField(
        verbose_name="Прекратить рассылку уведомлений по СМС", default=False
    )
    stop_sending_email = models.BooleanField(
        verbose_name="Прекратить рассылку уведомлений по email", default=False
    )

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"
        indexes = (
            models.Index(Upper("email"), name="email_idx"),
            GinIndex(
                fields=["email"],
                opclasses=["gin_trgm_ops"],
                name="email_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("email"), name="gin_trgm_ops"),
                name="email_up_gin_idx",
            ),
        )

    def __str__(self):
        return f"{self.username}"

    def get_fio(self):
        """Получение ФИО пользователя"""
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    def save(self, *args, **kwargs):
        if self.email == "":
            self.email = None
        return super().save(*args, **kwargs)

    def get_session_auth_hash(self, **kwargs):
        """Получение хэша при авторизации с телефона, вместо self.password вторым аргументом None"""
        phone = kwargs.get("phone")
        secret = None if phone else self.password
        key_salt = "users.models.User.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            secret,
            algorithm="sha512",
        ).hexdigest()
