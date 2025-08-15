import datetime

from django.utils import timezone
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from ..constants import OTP_TOKEN_VALIDATION_TIME
from ..models import OTPToken


class ValidateOTPToken(serializers.ModelSerializer):
    """Сериализатор для валидации токена"""

    phone = PhoneNumberField(label="Номер телефона")

    class Meta:
        model = OTPToken
        fields = ("phone", "uid", "otp")

    def validate(self, attrs):
        super().validate(attrs)
        phone = attrs["phone"]
        otp = attrs["otp"]
        uid = attrs["uid"]
        created_diff = timezone.now() - datetime.timedelta(minutes=OTP_TOKEN_VALIDATION_TIME)
        tokens = OTPToken.objects.filter(
            phone=phone, otp=otp, uid=uid, used=False, created__gte=created_diff
        )
        if tokens.exists():
            OTPToken.objects.filter(phone=phone, otp=otp).update(used=True)
            OTPToken.objects.filter(phone=phone, used=False).delete()
            return attrs
        expired_tokens = OTPToken.objects.filter(
            phone=phone, otp=otp, used=False, created__lt=created_diff
        )
        if expired_tokens:
            raise serializers.ValidationError("Ваш код авторизации истек")
        raise serializers.ValidationError("Неправильный код авторизации")
