from PIL import ImageFilter


class Blur:
    """Блюр."""

    def __init__(self, radius) -> None:
        """Инициализация."""
        self.radius = radius

    def process(self, img) -> None:
        """Процессинг."""
        return img.filter(ImageFilter.GaussianBlur(radius=self.radius))
