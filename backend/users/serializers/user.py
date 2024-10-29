from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.constants import TOKEN_INVALID
from users.models import OTPToken, User
from users.statuses import (
    USER_WITH_THIS_EMAIL_ALREADY_EXISTS,
    USER_WITH_THIS_PHONE_ALREADY_EXISTS,
)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

    class Meta:
        model = User
        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "user_permissions",
            "groups",
            "is_active",
            "is_staff",
        )


class UserEmailLoginSerializer(serializers.Serializer):
    """Сериализатор для логина по email."""

    email = serializers.EmailField(required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="ID токена", required=True)

    class Meta:
        fields = ("phone", "otp", "uid")


class UserPhoneRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации по номеру телефона."""

    phone = PhoneNumberField(label="Номер телефона", required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="ID токена", required=True)
    first_name = serializers.CharField(label="Имя", required=True)
    last_name = serializers.CharField(label="Фамилия", required=True)
    patronymic = serializers.CharField(label="Отчество", required=True)
    email = serializers.EmailField(label="Email", required=True)
    receive_advertising_notifications = serializers.BooleanField(
        label="Получать рекламные уведомления",
        default=False,
    )

    class Meta:
        model = User
        fields = (
            "phone",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "otp",
            "uid",
            "receive_advertising_notifications",
        )

    def validate(self, attrs):
        """Валидация."""
        super().validate(attrs)
        phone = attrs["phone"]
        email = attrs["email"]
        otp = attrs["otp"]
        uid = attrs["uid"]
        if not OTPToken.objects.filter(phone=phone, otp=otp, uid=uid, used=True).last():
            raise serializers.ValidationError(TOKEN_INVALID)
        if User.objects.filter(phone=phone):
            raise serializers.ValidationError(USER_WITH_THIS_PHONE_ALREADY_EXISTS)
        if User.objects.filter(email=email):
            raise serializers.ValidationError(USER_WITH_THIS_EMAIL_ALREADY_EXISTS)
        return attrs


class UserPhoneLoginSerializer(serializers.Serializer):
    """Сериализатор для логина по номеру телефона."""

    phone = PhoneNumberField(label="Номер телефона", required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="ID токена", required=True)

    class Meta:
        fields = ("phone", "otp", "uid")

    def validate(self, attrs):
        """Валидация."""
        super().validate(attrs)
        phone = attrs["phone"]
        otp = attrs["otp"]
        uid = attrs["uid"]
        if not OTPToken.objects.filter(phone=phone, otp=otp, uid=uid, used=True).last():
            raise serializers.ValidationError(TOKEN_INVALID)
        return attrs


class ChangeUserSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пользователя."""

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    phone = PhoneNumberField(label="Номер телефона")
    password = serializers.CharField(required=False, validators=[validate_password])
    password2 = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "avatar",
            "first_name",
            "last_name",
            "patronymic",
            "email",
            "phone",
            "password",
            "password2",
            "passport_number",
            "passport_serial",
            "birth_date",
            "gender",
        )
        extra_kwargs = {
            "first_name": {"allow_blank": False},
            "last_name": {"allow_blank": False},
            "email": {"required": False, "allow_blank": False},
            "phone": {"required": False, "allow_blank": False},
        }

    def validate(self, attrs):
        """Валидация."""
        if attrs.get("password") and not attrs.get("password2"):
            raise serializers.ValidationError({"password2": "Подтвердите пароль"})

        if (
            attrs.get("password")
            and attrs.get("password2")
            and (attrs["password"] != attrs["password2"])
        ):
            raise serializers.ValidationError({"password": "Пароли должны совпадать"})

        return attrs

    def save(self, **kwargs):
        """Сохранение."""
        password = self.validated_data.get("password")
        if password:
            self.instance.set_password(password)
            self.validated_data.pop("password")
        super().save()


class UserUsernameLoginSerializer(serializers.Serializer):
    """Сериализатор для логина по username."""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        fields = (
            "username",
            "password",
        )
