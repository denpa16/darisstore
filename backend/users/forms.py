from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField, EmailField

from users.models.user import User


class CreationForm(UserCreationForm):
    """Форма для создания пользователя."""

    email = EmailField(label="Отчество", required=False)
    patronymic = CharField(label="Отчество", required=False)

    class Meta:
        model = User
        fields = ("patronymic", "email")


class ChangeForm(UserChangeForm):
    """Форма для изменения пользователя."""

    email = EmailField(label="Email", required=False)

    class Meta:
        model = User
        fields = ("email",)
