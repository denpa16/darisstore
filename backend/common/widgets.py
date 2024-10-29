from django.forms.widgets import HiddenInput, MultiWidget, Textarea, TextInput


class PpoiWidget(MultiWidget):
    """Виджет для точки."""

    template_name = "common/widgets/ppoi.html"

    def __init__(self, attrs=None) -> None:
        """Инициализация."""
        _widgets = (TextInput(attrs=attrs), HiddenInput(attrs=attrs))
        super().__init__(widgets=_widgets, attrs={"class": "PpoiField__input", **(attrs or {})})

    def decompress(self, value) -> list:
        """Decompress."""
        if value is None:
            return []
        return value

    def get_context(self, name, value, attrs):
        """Получение контекста."""
        return super().get_context(name, value, attrs)

    class Media:
        css = {"screen": ("common/css/ppoi-widget.css",)}
        js = ("common/js/ppoi-widget.js",)


class PolygonWidget(MultiWidget):
    """Виджет для обводки."""

    template_name = "common/widgets/polygon.html"

    def __init__(self, attrs=None) -> None:
        """Инициализация."""
        _widgets = (
            Textarea(attrs=attrs),
            HiddenInput(attrs=attrs),
            HiddenInput(attrs=attrs),
            HiddenInput(attrs=attrs),
        )
        super().__init__(widgets=_widgets, attrs={"class": "js-sc-i", **(attrs or {})})

    def decompress(self, value) -> list:
        """Decompress."""
        if value is None:
            return []
        return value

    class Media:
        css = {"screen": ("common/css/polygon-widget.css",)}
        js = ("common/js/polygon-widget.js",)
