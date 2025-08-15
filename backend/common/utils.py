from __future__ import annotations

import datetime
from collections import defaultdict
from typing import Optional, List, Any
from django.utils import timezone

import functools
import math
from random import sample
from itertools import groupby

from django.db.models import TextField, Q
from django.forms import FileField


def floor(number, digits=0):
    if number is None:
        return None
    n = 10 ** -digits
    return round(math.floor(number / n) * n, digits)


def ceil(number, digits=0):
    if number is None:
        return None
    n = 10 ** -digits
    return round(math.ceil(number / n) * n, digits)


def rgetattr(obj, attr, *args):
    # noinspection PyShadowingNames
    def _getattr(obj, attr):
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


def get_icon_content(icon: Optional[FileField]) -> Optional[TextField]:
    """Получение содержимого иконки экземпляра модели."""
    icon_content = ""

    if icon:
        icon_content = icon.read()
        if isinstance(icon_content, bytes):
            icon_content = icon_content.decode("utf-8")
        icon_content.replace("\n", "").replace("b'", "")
        if icon_content.endswith("'"):
            icon_content = icon_content[:-1]

    return icon_content


def get_completion_quarter(date: datetime.datetime) -> int | None:
    """Получение квартала сдачи."""
    if date:
        return math.ceil(date.month / 3.0)
    else:
        return None


def get_completion_year(date: datetime.datetime) -> int | None:
    """Получение года сдачи."""
    if date:
        return date.year
    else:
        return None


def get_completion_date_filter(value: str) -> Q:
    """Создание фильтра по году сдачи и кварталу."""
    date_filter = Q()
    dates = value.split(",")
    for date in dates:
        try:
            year, quarter = date.split("-")
            date_filter |= Q(completion_year=year, completion_quarter=quarter)
        except ValueError:
            year = date.split("-")[0]
            date_filter |= Q(completion_year=year)
    return date_filter


def get_completion_dates_specs(comissioning_dates) -> list:
    """Получение спеков сроков сдачи по датам."""
    now = timezone.now()
    specs = []
    if comissioning_dates:
        # проверяем самую раннюю дату - если она меньше текущей - значит квартиры с ключами
        if comissioning_dates[0] < timezone.now():
            specs.append(
                {
                    "label": "С ключами",
                    "value": "released",
                    "subgroups": []
                }
            )
        # получаем даты после текущего года
        future_dates = [date for date in comissioning_dates if date.year > now.year]
        # получаем года вместе с кварталами в них
        if len(future_dates) > 1:
            grouped_dates = group_quarters_by_year(future_dates[:-1])
            for year, quarters in grouped_dates.items():
                if year > now.year:
                    specs.append(
                        {
                            "label": year,
                            "value": year,
                            "subgroups": quarters
                        }
                    )
            specs.append(
                {
                    "label": f"{future_dates[-1].year} и больше",
                    "value": future_dates[-1].year,
                    "subgroups": []
                }
            )
        else:
            grouped_dates = group_quarters_by_year(future_dates)
            for year, quarters in grouped_dates.items():
                if year > now.year:
                    specs.append(
                        {
                            "label": year,
                            "value": year,
                            "subgroups": quarters
                        }
                    )
    return specs


def get_completion_dates_facets(comissioning_dates) -> list:
    """Получение фасетов сроков сдачи по датам."""
    now = timezone.now()
    facets = []
    if comissioning_dates:
        # проверяем самую раннюю дату - если она меньше текущей - значит квартиры с ключами
        if comissioning_dates[0] < timezone.now():
            facets.append(
                {
                    "choices": "released",
                    "subgroups": [
                        {
                            "name": "quarters",
                            "choices": []
                        }
                    ]
                }
            )
        # получаем даты после текущего года
        future_dates = [date for date in comissioning_dates if date.year > now.year]
        # получаем года вместе с кварталами в них
        if len(future_dates) > 1:
            grouped_dates = group_quarters_by_year(future_dates[:-1])
            for year, quarters in grouped_dates.items():
                if year > now.year:
                    facets.append(
                        {
                            "choices": year,
                            "subgroups": [
                                {
                                    "name": "quarters",
                                    "choices": quarters
                                }
                            ]
                        }
                    )
            facets.append(
                {
                    "choices": future_dates[-1].year,
                    "subgroups": [
                        {
                            "name": "quarters",
                            "choices": []
                        }
                    ]
                }
            )
        else:
            grouped_dates = group_quarters_by_year(future_dates)
            for year, quarters in grouped_dates.items():
                if year > now.year:
                    facets.append(
                        {
                            "choices": year,
                            "subgroups": [
                                {
                                    "name": "quarters",
                                    "choices": quarters
                                }
                            ]
                        }
                    )
    return facets


def group_quarters_by_year(dates: List[datetime.datetime]) -> dict[int, List[Any]]:
    dates_datas = defaultdict(set)  # Using a set to prevent duplicate months
    for date in dates:
        dates_datas[date.year].add(date.month)  # No need for a try-except
    # Converting sets to sorted lists before returning
    return {year: sorted(list(months)) for year, months in dates_datas.items()}


def group_buildings_by_project(data: List[Any]) -> dict[Any, List[Any]]:
    """Группировка корпусов по проектам."""
    dict_data = defaultdict(set)  # Using a set to prevent duplicate months
    for instance in data:
        dict_data[(instance[0]), instance[1]].add(
            (instance[2], instance[3]))  # No need for a try-except
    return {project: sorted(list(buildings)) for project, buildings in dict_data.items()}


def get_range_filter(name: str, value: slice) -> Q:
    """Фильтр по диапазону значений."""
    value_min, value_max = value.start, value.stop
    range_filter = Q()
    if value_min:
        range_filter &= Q(**{f"{name}__gte": value_min})
    if value_max:
        range_filter &= Q(**{f"{name}__lte": value_max})
    return range_filter

def get_russian_weekday(day: int) -> str:
    weekday_dict = {
        0: "пн",
        1: "вт",
        2: "ср",
        3: "чт",
        4: "пт",
        5: "сб",
        6: "вс"
    }
    return weekday_dict[day]
