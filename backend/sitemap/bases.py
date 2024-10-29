from django.contrib.sitemaps import Sitemap
from django.core.handlers.wsgi import WSGIRequest


class SitemapMeta(type):
    """Добавляет внутренние классы в список элементов sitemap."""

    def __new__(cls, name: str, bases: tuple, attrs: dict) -> "SitemapMeta":
        """Создание класса."""
        maps = {}
        for attr in attrs.values():
            if (
                not isinstance(attr, str)
                and attr.__name__.lower().count("sitemap")
                and getattr(attr, "name", None) is not None
            ):
                maps[attr.name] = attr
        attrs["maps"] = maps
        return super().__new__(cls, name, bases, attrs)


class BaseSitemap(Sitemap):
    """Sitemap с базовой конфигурацией."""

    name = None
    objects = None
    changefreq = "daily"
    priority = 1.0

    def __init__(self, request: WSGIRequest) -> None:
        """Инициализация класса."""
        self.request = request

    def items(self) -> objects:
        """Объекты."""
        return self.objects

    def location(self, obj: str) -> str:
        """Путь."""
        return f"/{self.name}/{obj}/"
