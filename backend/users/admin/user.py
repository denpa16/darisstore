from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from ..models import User
from ..forms import ChangeForm, CreationForm


@register(User)
class UserAdmin(UserAdmin):
    """Пользователь"""

    form = ChangeForm
    add_form = CreationForm
    list_display = (
        "id",
        "email",
        "username",
        "is_staff",
        "is_active",
        "is_superuser",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "avatar",
                    "first_name",
                    "last_name",
                    "patronymic",
                    "gender",
                    "email",
                    "phone",
                    "phone_additional",
                    "resident",
                    "passport_number",
                    "passport_serial",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "gender",
                    "email",
                    "phone",
                    "phone_additional",
                    "resident",
                    "passport_number",
                    "passport_serial",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
