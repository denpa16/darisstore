from django.contrib.auth import get_user_model

from users.models import OTPToken

User = get_user_model()


def custom_phone_register(*args, **kwargs):
    """Кастомная регистрациия по телефону."""
    phone = kwargs.pop("phone")
    uid = kwargs.pop("uid")
    otp = kwargs.pop("otp")
    token = OTPToken.objects.filter(uid=uid, phone=phone, otp=otp).first()
    if not token:
        return None
    return User.objects.create(is_active=True, **kwargs)
