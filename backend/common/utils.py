from __future__ import annotations

import functools
import math
import os
import re
import xml.etree.ElementTree as ET
from random import sample
from typing import TYPE_CHECKING

from django.core.files.storage import default_storage
from django.db.models import ImageField, Q, TextField
from PIL import Image

if TYPE_CHECKING:
    import datetime

    from django.forms import FileField


def floor(number, digits=0):
    """Получение целого, ограниченного снизу."""
    if number is None:
        return None
    n = 10**-digits
    return round(math.floor(number / n) * n, digits)


def ceil(number, digits=0):
    """Получение целого, ограниченного сверху."""
    if number is None:
        return None
    n = 10**-digits
    return round(math.ceil(number / n) * n, digits)


def rgetattr(obj, attr, *args) -> None:
    """Rgetattr."""

    def _getattr(obj, attr) -> None:
        if obj:
            return getattr(obj, attr, *args)
        return None

    return functools.reduce(_getattr, [obj, *attr.split(".")])


def generate_code(length: int = 4) -> str:
    """Возвращает строку из n случайных чисел."""
    return "".join([str(x) for x in sample(range(10), length)])


@functools.lru_cache
def get_russian_month(
    month: int,
    slice_stop: int | None = None,
    title: bool = False,
    case: bool = False,
) -> str:
    """Получение названия месяца по году."""
    month_dict = {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь",
    }
    month = month_dict.get(month)[:slice_stop]
    if title:
        month = month.title()
    if case:
        month = month.replace(month[-1], "я") if month[-1] in ["ь", "й"] else month + "a"

    return month


def get_svg_content(svg: FileField | None) -> TextField | None:
    """Получение содержимого svg экземпляра модели."""
    svg_content = ""

    if svg:
        svg_content = svg.read()
        if isinstance(svg_content, bytes):
            svg_content = svg_content.decode("utf-8")
        svg_content.replace("\n", "").replace("b'", "")
        if svg_content.endswith("'"):
            svg_content = svg_content[:-1]

    return svg_content


def get_completion_quarter(date: datetime.datetime) -> int | None:
    """Получение квартала сдачи."""
    if date:
        return math.ceil(date.month / 3.0)
    return None


def get_completion_year(date: datetime.datetime) -> int | None:
    """Получение года сдачи."""
    if date:
        return date.year
    return None


def get_range_filter(name: str, value: slice) -> Q:
    """Фильтр по диапазону значений."""
    value_min, value_max = value.start, value.stop
    range_filter = Q()
    if value_min:
        range_filter &= Q(**{f"{name}__gte": value_min})
    if value_max:
        range_filter &= Q(**{f"{name}__lte": value_max})
    return range_filter


def camel_case_to_snake_case(name: str) -> str:
    """Camel case to snake case method."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def escape_quotes(string: str) -> str:
    """Экранирование двойных кавычек в строке."""
    return string.replace('"', '\\"')


def get_svg_size(file) -> tuple:
    """Получение размеров svg-файла."""
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        viewBox = root.attrib.get("viewBox")
        _, _, width, height = map(float, viewBox.split(" "))
    except Exception:
        width, height = None, None
    if width and height:
        return float(width), float(height)
    f = file.file.read().decode("utf-8")
    m = re.search(r'(?<=viewBox=)"([\d\s.]+)"', f)
    if m:
        viewbox = m.group(0)
        viewbox = viewbox.replace('"', "")
        *zeros, width, height = viewbox.split()
    if width and height:
        return float(width), float(height)
    return width, height


def get_image_size(file) -> tuple:
    """Получение размеров изображения."""
    try:
        image = Image.open(default_storage.open(file.name))
    except Exception:
        return None, None
    else:
        return image.width, image.height


def get_file_sizes(file) -> tuple:
    """Получение размера файла."""
    if file:
        _, ext = os.path.splitext(file.url)
        ext = ext[1:].lower()
        if ext in ("jpg", "jpeg", "png", "webp"):
            return get_image_size(file)
        if ext == "svg":
            return get_svg_size(file)
    return None, None


def get_mime_type(image: ImageField):
    """Получение формата изображения."""
    image_name = image.name.lower()
    if image_name.endswith((".jpg", ".jpeg")):
        return "image/jpeg"
    if image_name.endswith(".png"):
        return "image/png"
    # По умолчанию для неизвестных форматов
    return "application/octet-stream"
