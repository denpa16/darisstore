from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from ..models import OTPToken

User = get_user_model()


class PhoneBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        phone = kwargs.get("phone", False)
        if phone:
            uid = kwargs.get("uid")
            otp = kwargs.get("otp")
            token: OTPToken = OTPToken.objects.filter(uid=uid, phone=phone, otp=otp).first()
            if not token:
                return None
            user = User.objects.filter(phone=phone).first()
            if not user:
                user = User.objects.create_user(username=phone, phone=phone, is_active=True)
            return user
