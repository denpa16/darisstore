import datetime

import pytz
from rest_framework import serializers

from users.models import EmailOTPToken


class CreateEmailOTPToken(serializers.ModelSerializer):
    """Сериализатор для создания токена для email."""

    class Meta:
        model = EmailOTPToken
        fields = ("email", "uid")

    def validate_email(self, email):
        """Валидация email."""
        attempts_count = 10
        today_min = pytz.utc.localize(
            datetime.datetime.combine(datetime.datetime.now(tz=pytz.utc).date(), datetime.time.min),
        )
        today_max = pytz.utc.localize(
            datetime.datetime.combine(datetime.datetime.now(tz=pytz.utc).date(), datetime.time.max),
        )
        otps = EmailOTPToken.objects.filter(email=email, created__range=(today_min, today_max))
        if otps.count() >= attempts_count:
            msg = "Превышено максимальное количество попыток входа."
            raise serializers.ValidationError(msg)
        return email

    def save(self):
        """Сохранение."""
        return EmailOTPToken.create(self.data["email"])
