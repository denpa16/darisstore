import datetime

from django.utils import timezone
from rest_framework import serializers

from ..constants import OTP_TOKEN_VALIDATION_TIME
from ..models import EmailOTPToken


class ValidateEmailOTPToken(serializers.ModelSerializer):
    """Сериализатор для валидации токена для email"""

    class Meta:
        model = EmailOTPToken
        fields = ("email", "uid", "otp")

    def validate(self, attrs):
        super().validate(attrs)
        email = attrs["email"]
        otp = attrs["otp"]
        uid = attrs["uid"]
        created_diff = timezone.now() - datetime.timedelta(minutes=OTP_TOKEN_VALIDATION_TIME)
        tokens = EmailOTPToken.objects.filter(
            email=email, otp=otp, uid=uid, used=False, created__gte=created_diff
        )
        if tokens.exists():
            EmailOTPToken.objects.filter(email=email, otp=otp).update(used=True)
            EmailOTPToken.objects.filter(email=email, used=False).delete()
            return attrs
        expired_tokens = EmailOTPToken.objects.filter(
            email=email, otp=otp, used=False, created__lt=created_diff
        )
        if expired_tokens:
            raise serializers.ValidationError("Ваш код авторизации истек")
        raise serializers.ValidationError("Неправильный код авторизации")
