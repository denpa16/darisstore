from django.contrib.auth import authenticate, get_user_model, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from common.auth import custom_login
from common.responses import Response
from users.serializers import (
    UserPhoneLoginSerializer,
    UserPhoneRegisterSerializer,
    UserSerializer,
)
from users.statuses import (
    USER_NOT_FOUND,
)
from users.utils import custom_phone_register

User = get_user_model()


@extend_schema(tags=["User"])
class UserViewSet(GenericViewSet):
    """API для взаимодействия с личным кабинетом."""

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        """Сериализатор."""
        if self.action == self.phone_register.__name__:
            return UserPhoneRegisterSerializer
        if self.action == self.phone_login.__name__:
            return UserPhoneLoginSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        """Список пользователей."""
        if not bool(request.user and request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer: UserSerializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """Получение пользователя."""
        if not bool(request.user and request.user.is_authenticated):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer: UserSerializer = self.get_serializer(instance=request.user)
        return Response(data=serializer.data)

    @action(methods=["POST"], detail=False, url_name="phone_register", permission_classes=[])
    def phone_register(self, request):
        """Регистрация пользователя по телефону после валидации кода."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = custom_phone_register(**serializer.validated_data)
        if not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        custom_login(request, user, backend="users.backends.phone.PhoneBackend")
        return Response(data=UserSerializer(instance=user).data, status=status.HTTP_201_CREATED)

    @action(methods=["POST"], detail=False, url_name="phone_login", permission_classes=[])
    def phone_login(self, request):
        """Авторизация по телефону после валидации кода."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not User.objects.filter(phone=serializer.validated_data["phone"]):
            return Response(status=status.HTTP_404_NOT_FOUND, message=USER_NOT_FOUND)
        user = authenticate(request, **serializer.data)
        custom_login(request, user, backend="users.backends.phone.PhoneBackend")
        return Response(status=status.HTTP_200_OK, data=UserSerializer(instance=user).data)

    @action(detail=False, methods=["GET"])
    def logout(self, request):
        """Логаут."""
        logout(request)
        return Response(status=status.HTTP_200_OK)
