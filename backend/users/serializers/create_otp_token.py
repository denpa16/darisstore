import datetime

import pytz
from phonenumber_field.serializerfields import PhoneNumberField
from pytz import utc
from rest_framework import serializers

from users.constants import OTPTokenType
from users.models import OTPToken


class CreateOTPToken(serializers.ModelSerializer):
    """Сериализатор для создания токена."""

    phone = PhoneNumberField(label="Номер телефона", required=True)
    type = serializers.ChoiceField(
        label="Тип подтверждения",
        choices=OTPTokenType.choices,
        default=OTPTokenType.LOGIN,
        write_only=True,
    )

    class Meta:
        model = OTPToken
        fields = ("phone", "uid", "type")

    def validate_phone(self, phone):
        """Валидация номера телефона."""
        attempts_count = 10
        today_min = utc.localize(
            datetime.datetime.combine(datetime.datetime.now(tz=pytz.utc).date(), datetime.time.min),
        )
        today_max = utc.localize(
            datetime.datetime.combine(datetime.datetime.now(tz=pytz.utc).date(), datetime.time.max),
        )
        otps = OTPToken.objects.filter(phone=phone, created__range=(today_min, today_max))
        if otps.count() >= attempts_count:
            msg = "Превышено максимальное количество попыток входа."
            raise serializers.ValidationError(msg)
        return phone

    def save(self):
        """Сохранение."""
        return OTPToken.create(self.data["phone"], self.validated_data["type"])
