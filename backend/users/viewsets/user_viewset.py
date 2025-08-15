from django.contrib.auth import authenticate, get_user_model, logout
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.auth import custom_login

from ..serializers import (
    ChangeUserSerializer,
    UserEmailLoginSerializer,
    UserLoginOrRegisterSerializer,
    UserSerializer,
)

User = get_user_model()


@extend_schema(tags=["User"])
class UserViewSet(GenericViewSet):
    """API для взаимодействия с личным кабинетом"""

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ("register_phone", "phone_login"):
            return UserLoginOrRegisterSerializer
        if self.action == "change":
            return ChangeUserSerializer
        if self.action == "email_login":
            return UserEmailLoginSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        if not bool(request.user and request.user.is_authenticated):
            return Response({"ok": False, "errors": "not authorized"})
        serializer: UserSerializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        if not bool(request.user and request.user.is_authenticated):
            return Response({"ok": False, "errors": "not authorized"})

        serializer: UserSerializer = self.get_serializer(instance=request.user)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False, url_name="register_phone", permission_classes=[])
    def register_phone(self, request):
        """Регистрация пользователя после валидации кода"""
        serializer: UserLoginOrRegisterSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"ok": False, "errors": serializer.errors})
        if User.objects.filter(phone=serializer.validated_data["phone"]).exists():
            return Response(
                {
                    "ok": False,
                    "errors": "Пользователь с таким номером телефона "
                    "уже зарегистрирован в системе.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, **serializer.data)
        custom_login(request, user, backend="users.backends.phone.PhoneBackend")
        return Response(UserSerializer(instance=user).data)

    @action(methods=["POST"], detail=False, url_name="email_login", permission_classes=[])
    def email_login(self, request):
        """Авторизация по почте"""
        serializer: UserEmailLoginSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"ok": False, "errors": serializer.errors})
        user = authenticate(request, **serializer.data)
        custom_login(request, user, backend="users.backends.email_backend.EmailBackend")
        if not user.is_anonymous and user.is_authenticated:
            return Response(
                status=status.HTTP_200_OK,
                data=UserSerializer(instance=user).data,
            )
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={"ok": False, "errors": "Неверно указаны значения"},
        )

    @action(methods=["POST"], detail=False, url_name="phone_login", permission_classes=[])
    def phone_login(self, request):
        """Авторизация по телефону"""
        serializer: UserLoginOrRegisterSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"ok": False, "errors": serializer.errors})
        user = authenticate(request, **serializer.data)
        custom_login(request, user, backend="users.backends.phone.PhoneBackend")
        return Response(status=status.HTTP_200_OK, data=UserSerializer(instance=user).data)

    @action(detail=False, methods=["GET"])
    def logout(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=["PATCH"])
    def change(self, request):
        if not bool(request.user and request.user.is_authenticated):
            return Response({"ok": False, "errors": "not authorized"})
        user = request.user
        serializer = self.get_serializer(instance=user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
