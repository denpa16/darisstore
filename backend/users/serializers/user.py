from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


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


class UserLoginOrRegisterSerializer(serializers.Serializer):
    """Сериализатор для логина по номеру телефона."""

    phone = PhoneNumberField(label="Номер телефона", required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="ID токена", required=True)

    class Meta:
        fields = ("phone", "otp", "uid")


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
