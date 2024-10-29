from sitemap.bases import BaseSitemap, SitemapMeta


class SiteSitemap(metaclass=SitemapMeta):
    """Sitemap Site."""

    class StaticSitemap(BaseSitemap):
        """Карта статических страниц."""

        name = "static"

        def items(self) -> list:
            """Объекты."""
            return [
                "/",
            ]

        def location(self, obj: str) -> str:
            """Путь."""
            return obj
