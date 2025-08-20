from rest_framework.routers import SimpleRouter

from users.viewsets import UserViewSet, OTPTokenViewSet

router = SimpleRouter()

# A -Z sorting
router.register(r"otp", OTPTokenViewSet, "otp")
router.register(r"users", UserViewSet, "users")
