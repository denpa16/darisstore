import datetime

from phonenumber_field.serializerfields import PhoneNumberField
from pytz import utc
from rest_framework import serializers

from ..constants import OTPTokenType
from ..models import OTPToken


class CreateOTPToken(serializers.ModelSerializer):
    """Сериализатор для создания токена"""

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
        today_min = utc.localize(
            datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        )
        today_max = utc.localize(
            datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        )
        otps = OTPToken.objects.filter(phone=phone, created__range=(today_min, today_max))
        if otps.count() >= 10:
            raise serializers.ValidationError("Превышено максимальное количество попыток входа.")
        return phone

    def save(self, commit=True):
        instance = OTPToken.create(self.data["phone"], self.validated_data["type"])
        return instance
