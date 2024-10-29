from django.contrib import admin

from common.models import APIRequestLog


@admin.register(APIRequestLog)
class APIRequestLogAdmin(admin.ModelAdmin):
    """Логи зопросов к Django REST Framework API."""

    date_hierarchy = "requested_at"
    list_display = (
        "id",
        "requested_at",
        "response_ms",
        "status_code",
        "user",
        "view_method",
        "path",
        "remote_addr",
        "host",
    )
    ordering = ("-requested_at",)
    list_filter = ("view_method", "status_code")
    search_fields = (
        "user__email",
        "username_persistent",
        "path",
        "view",
        "view_method",
        "remote_addr",
        "host",
        "method",
        "query_params",
        "data",
        "response",
        "errors",
    )
    raw_id_fields = ("user",)
