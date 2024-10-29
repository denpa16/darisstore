from typing import NoReturn

from rest_framework.response import Response


class GetIPMiddleware:
    """GetIPMiddleware."""

    def __init__(self, get_response) -> NoReturn:
        """Инциализация."""
        self.get_response = get_response
        super().__init__()

    def __call__(self, request) -> Response:
        """Вызов."""
        x_forwarded_for = request.META.get("X-Real-IP", None)
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR", None)
        request.ip = ip
        return self.get_response(request)
