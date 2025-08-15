from rest_framework.routers import DefaultRouter

from users.viewsets import EmailOTPTokenViewSet, OTPTokenViewSet, UserViewSet

router = DefaultRouter()

# users
router.register(r"users", UserViewSet, "users")
