from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from users.models import EmailOTPToken

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """Бэкенд для аутентификации по email и одноразовому коду."""

    def authenticate(self, request, **kwargs):
        """Кастомный метод аутентификации."""
        email = kwargs.get("email", False)
        if email:
            uid = kwargs.get("uid")
            otp = kwargs.get("otp")
            token: EmailOTPToken = EmailOTPToken.objects.filter(
                uid=uid,
                email=email,
                otp=otp,
            ).first()
            if not token:
                return None
            user = UserModel.objects.filter(email=email).first()
            if not user:
                user = UserModel.objects.create_user(username=email, email=email, is_active=True)
            return user
        return None
