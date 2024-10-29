from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.postgres.fields import ArrayField, RangeField
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.forms import SelectMultiple

from .form_fields import (
    FloatRangeFormField,
    InclusiveNumericRange,
    IntegerRangeFormField,
    PolygonFormField,
    PpoiFormField,
)
from .utils import rgetattr


class PolygonField(models.Field):
    """Поле обводки."""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize a PolygonField instance."""
        if "source" not in kwargs or not isinstance(kwargs["source"], str):
            msg = "Polygon field source isn't set or not correct"
            raise ImproperlyConfigured(msg)
        new_kwargs = kwargs.copy()
        del new_kwargs["source"]
        self.source = kwargs["source"]
        super().__init__(*args, **new_kwargs)

    def deconstruct(self):
        """Deconstruct the field for migrations."""
        path, name, args, kwargs = super().deconstruct()
        kwargs["source"] = self.source
        return path, name, args, kwargs

    def get_internal_type(self):
        """Get internal value."""
        return "TextField"

    def formfield(self, **kwargs):
        """Get formfield."""
        defaults = {"form_class": PolygonFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def get_prep_value(self, value):
        """Get prepare value."""
        if value in self.empty_values:
            return ""
        if isinstance(value, str):
            return super().get_prep_value(value)
        return super().get_prep_value(value[0])

    def value_from_object(self, obj):
        """Get value from object."""
        field_image = rgetattr(obj, self.source)
        if field_image:
            try:
                if not isinstance(field_image, ImageFieldFile):
                    field_image = ImageFieldFile(
                        field_image.instance,
                        field_image.field,
                        field_image.name,
                    )
                width = field_image.width
                height = field_image.height
                if width is None and height is None:
                    width_field = "{}_width".format(self.source.split(".")[1])
                    height_field = "{}_height".format(self.source.split(".")[1])
                    width = getattr(field_image.instance, width_field, None)
                    height = getattr(field_image.instance, height_field, None)
                field_image = field_image.url
            except Exception:
                field_image = None
                width = None
                height = None
        else:
            field_image = None
            width = None
            height = None
        return getattr(obj, self.attname), field_image, width, height

    def value_to_string(self, obj):
        """Convert value to string."""
        return getattr(obj, self.attname)


class PpoiField(models.Field):
    """Поле точки."""

    def __init__(self, *args, **kwargs) -> None:
        """Инициализация."""
        if "source" not in kwargs or not isinstance(kwargs["source"], str):
            msg = "Ppoi field source isn't set or not correct"
            raise ImproperlyConfigured(msg)
        new_kwargs = kwargs.copy()
        del new_kwargs["source"]
        self.source = kwargs["source"]
        new_kwargs["max_length"] = 50
        super().__init__(*args, **new_kwargs)

    def deconstruct(self) -> None:
        """Deconstruct the field for migrations."""
        path, name, args, kwargs = super().deconstruct()
        kwargs["source"] = self.source
        return path, name, args, kwargs

    def get_internal_type(self) -> None:
        """Get tipe of field."""
        return "CharField"

    def formfield(self, **kwargs):
        """Get form for field."""
        defaults = {"form_class": PpoiFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)

    def get_prep_value(self, value):
        """Get prepared field."""
        if value in self.empty_values:
            return ""
        if isinstance(value, str):
            return super().get_prep_value(value)
        return super().get_prep_value(value[0])

    def value_from_object(self, obj):
        """Get imgae name from file."""
        field_image = rgetattr(obj, self.source)
        field_image = field_image.url if field_image else None
        return getattr(obj, self.attname), field_image

    def value_to_string(self, obj):
        """Value to str."""
        return getattr(obj, self.attname).split(",")


class ArraySelectMultiple(SelectMultiple):
    """Поле для множественного выбора из диапазона значений."""

    def value_omitted_from_data(self, data, files, name) -> bool:
        """Получение значения из невключченных значений."""
        return False


class ChoiceArrayField(ArrayField):
    """Поле для выбора из списка значений."""

    def formfield(self, **kwargs) -> None:
        """Форма."""
        defaults = {
            "form_class": forms.TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
            "widget": FilteredSelectMultiple(
                verbose_name=self.base_field.verbose_name,
                is_stacked=False,
            ),
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class FloatRangeField(RangeField):
    """Поле для диапазона чисел с плавающей точкой."""

    base_field = models.FloatField
    range_type = InclusiveNumericRange
    form_field = FloatRangeFormField

    def db_type(self, connection) -> str:
        """Тип поле для БД."""
        return "numrange"


class IntegerRangeField(RangeField):
    """Поле для диапазона целых чисел."""

    base_field = models.IntegerField
    range_type = InclusiveNumericRange
    form_field = IntegerRangeFormField

    def db_type(self, connection) -> str:
        """Тип поле для БД."""
        return "int4range"
