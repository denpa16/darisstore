from dataclasses import dataclass

from django.db import models

from config.settings import IMGPROXY_FULL_PATH, IMGPROXY_SECURE


@dataclass
class Spec:
    source: str
    width: int = 0
    height: int = 0
    blur: int = False
    default: str = "jpeg"
    crop: bool = False


class MultiImageMeta(models.base.ModelBase):
    def __new__(mcs, name, bases, dct):
        # нет карты нет обработки
        if "image_map" not in dct:
            return super().__new__(mcs, name, bases, dct)

        # инициализауия параметров
        for spec_name, spec in dct["image_map"].items():
            link = IMGPROXY_FULL_PATH
            if not IMGPROXY_SECURE:
                link += "/insecure"

            config = ""

            if spec.width and spec.height:
                config += f"/rs:auto:{spec.height}:{spec.width}/"

            if spec.blur:
                config += "blur:10/q:70/"

            dct[f"{spec_name}_config"] = config
            dct[f"{spec_name}_default"] = link + config + "plain/"

        return super().__new__(mcs, name, bases, dct)
