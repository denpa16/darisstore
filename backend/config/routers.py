from rest_framework.routers import SimpleRouter

from users.viewsets import EmailOTPTokenViewSet, OTPTokenViewSet, UserViewSet

router = SimpleRouter()


router.register(r"users", UserViewSet, "users")
router.register(r"otp_token", OTPTokenViewSet, "otp_token")
router.register(r"email_otp_token", EmailOTPTokenViewSet, "email_otp_token")
