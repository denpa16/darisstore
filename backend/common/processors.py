from PIL import ImageFilter


class Blur:
    def __init__(self, radius):
        self.radius = radius

    def process(self, img):
        return img.filter(ImageFilter.GaussianBlur(radius=self.radius))
