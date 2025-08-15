from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from ..models import EmailOTPToken

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs.get("email", False)
        if email:
            uid = kwargs.get("uid")
            otp = kwargs.get("otp")
            token: EmailOTPToken = EmailOTPToken.objects.filter(
                uid=uid, email=email, otp=otp
            ).first()
            if not token:
                return None
            user = UserModel.objects.filter(email=email).first()
            if not user:
                user = UserModel.objects.create_user(username=email, email=email, is_active=True)
            return user
