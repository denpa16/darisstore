from http import HTTPStatus
from typing import TYPE_CHECKING, Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.serializers import Serializer


class SoloModelViewSet(GenericViewSet):
    """Вьюсет для Solo модели."""

    def list(self, request: Request, *args: list[Any], **kwargs: dict[Any, Any]) -> Response:
        """List method."""
        queryset: type[QuerySet] = self.get_queryset()
        serializer: type[Serializer] = self.get_serializer(queryset.first())
        data: dict[str, Any] = serializer.data
        return Response(data=data, status=HTTPStatus.OK)
