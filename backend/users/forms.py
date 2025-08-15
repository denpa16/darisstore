from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import CharField

from users.models.user import User


class CreationForm(UserCreationForm):
    patronymic = CharField(label="Отчество")

    class Meta:
        model = User
        fields = ("patronymic", "email")


class ChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email",)
