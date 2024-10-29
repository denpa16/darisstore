from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response


class BaseLimitOffsetPagination(LimitOffsetPagination):
    """Базовая пагинация."""

    default_limit = 12


class BasePageNumberPagination(PageNumberPagination):
    """Постраничная пагинация."""

    page_size = 6
    page_query_param = "page"
    page_size_query_param = "page_size"

    def get_paginated_response(self, data):
        """Ответ пагинации."""
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "results": data,
            },
        )
