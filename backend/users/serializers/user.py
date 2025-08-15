from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="ID токена", required=True)

    class Meta:
        fields = ("phone", "otp", "uid")


class UserLoginOrRegisterSerializer(serializers.Serializer):
    phone = PhoneNumberField(label="Номер телефона", required=True)
    otp = serializers.CharField(label="Временный пароль", required=True)
    uid = serializers.UUIDField(label="ID токена", required=True)

    class Meta:
        fields = ("phone", "otp", "uid")


class ChangeUserSerializer(serializers.ModelSerializer):
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
        if attrs.get("password") and not attrs.get("password2"):
            raise serializers.ValidationError({"password2": "Подтвердите пароль"})

        if attrs.get("password") and attrs.get("password2"):
            if attrs["password"] != attrs["password2"]:
                raise serializers.ValidationError({"password": "Пароли должны совпадать"})

        return attrs

    def save(self, **kwargs):
        password = self.validated_data.get("password")
        if password:
            self.instance.set_password(password)
            self.validated_data.pop("password")
        super().save()
