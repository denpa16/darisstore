from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class PhoneLoginBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        phone = kwargs.get("phone", False)
        password = kwargs.get("password", False)
        if phone and password:
            user = User.objects.filter(phone=phone).first()
            if user:
                if user.check_password(password):
                    return user
        return None
