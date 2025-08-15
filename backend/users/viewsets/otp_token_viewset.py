from django.utils.timezone import now
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from ..models import EmailOTPToken, OTPToken
from ..serializers import (
    CreateEmailOTPToken,
    CreateOTPToken,
    ValidateEmailOTPToken,
    ValidateOTPToken,
)


@extend_schema(tags=["OTP_Token"])
class OTPTokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    """API для взаимодействия с СМС сервисом"""

    queryset = OTPToken.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOTPToken
        return ValidateOTPToken

    def create(self, request, *args, **kwargs):
        serializer: CreateOTPToken = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(commit=True)
        headers = self.get_success_headers(serializer.data)
        return Response(
            CreateOTPToken(instance=instance).data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(methods=["POST"], detail=False, url_name="validate_otp_token")
    def validate_otp_token(self, request):
        """Валидация токена"""
        serializer: ValidateOTPToken = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.session["phone"] = request.data.get("phone")
        request.session["phone_confirmed_time"] = now()
        return Response(serializer.data)


@extend_schema(tags=["Email OTP_Token"])
class EmailOTPTokenViewSet(mixins.CreateModelMixin, GenericViewSet):
    """API для подтверждения email"""

    queryset = EmailOTPToken.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateEmailOTPToken
        return ValidateEmailOTPToken

    def create(self, request, *args, **kwargs):
        serializer: CreateEmailOTPToken = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            CreateEmailOTPToken(instance=instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(methods=["POST"], detail=False, url_name="validate_otp_token")
    def validate_otp_token(self, request):
        """Валидация токена"""
        serializer: ValidateEmailOTPToken = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.session["email"] = request.data.get("email")
        request.session["email_confirmed_time"] = now()
        return Response(serializer.data)
