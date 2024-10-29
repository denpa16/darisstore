from django import forms
from django.contrib.postgres.forms import BaseRangeField
from django.core.exceptions import ValidationError
from django.forms import CharField, MultiValueField
from psycopg2.extras import NumericRange

from .widgets import PolygonWidget, PpoiWidget


class PolygonFormField(MultiValueField):
    """Форма для поля обводки."""

    widget = PolygonWidget

    default_error_messages = {"invalid": "Значение должно быть двумя числами, разделенными запятой"}

    def __init__(self, **kwargs) -> None:
        """Инициализация."""
        fields = (CharField(),)
        super().__init__(fields, **kwargs)

    def compress(self, data_list) -> None:
        """Compress."""
        return data_list


class PpoiFormField(MultiValueField):
    """Форма для поля точки."""

    widget = PpoiWidget

    default_error_messages = {"invalid": "Значение должно быть двумя числами, разделенными запятой"}

    def __init__(self, **kwargs) -> None:
        """Инициализация."""
        fields = (CharField(required=False), CharField(required=False))
        super().__init__(fields, require_all_fields=False, **kwargs)

    def compress(self, data_list) -> None:
        """Compress data."""
        return data_list

    def validate(self, value) -> None:
        """Валидация."""
        super().validate(value)
        if value[0] == "" or value is None:
            return
        parts = value[0].split(",")
        invalid_len = 2
        if not len(parts) == invalid_len:
            raise ValidationError(self.error_messages["invalid"], code="invalid")
        try:
            float(parts[0])
            float(parts[1])
        except ValueError as e:
            raise ValidationError(self.error_messages["invalid"], code="invalid") from e


class InclusiveNumericRange(NumericRange):
    """InclusiveNumericRange."""

    def __init__(self, lower=None, upper=None, bounds="[]", empty=False) -> None:
        """Инициализация."""
        super().__init__(lower, upper, bounds, empty)


class FloatRangeFormField(BaseRangeField):
    """Форма для Range float поля."""

    range_type = InclusiveNumericRange
    base_field = forms.FloatField


class IntegerRangeFormField(BaseRangeField):
    """Форма для Range integer поля."""

    range_type = InclusiveNumericRange
    base_field = forms.IntegerField
