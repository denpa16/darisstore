from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class PhoneLoginBackend(ModelBackend):
    """Бэкенд для аутентификации по телефону и паролю."""

    def authenticate(self, request, **kwargs):
        """Кастомный метод аутентификации."""
        phone = kwargs.get("phone", False)
        password = kwargs.get("password", False)
        if phone and password:
            user = User.objects.filter(phone=phone).first()
            if user and user.check_password(password):
                return user
        return None
