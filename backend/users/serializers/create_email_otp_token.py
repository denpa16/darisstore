from rest_framework import serializers

from ..models import EmailOTPToken
from .today_min_max import today_max, today_min


class CreateEmailOTPToken(serializers.ModelSerializer):
    """Сериализатор для создания токена для email"""

    class Meta:
        model = EmailOTPToken
        fields = ("email", "uid")

    def validate_email(self, email):
        otps = EmailOTPToken.objects.filter(email=email, created__range=(today_min, today_max))
        if otps.count() >= 10:
            raise serializers.ValidationError("Превышено максимальное количество попыток входа.")
        return email

    def save(self):
        instance = EmailOTPToken.create(self.data["email"])
        return instance
