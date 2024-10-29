from typing import NamedTuple
from urllib import request

import requests
import sentry_sdk
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile
from rest_framework import status

from .integrations import SMSCSMS
from .yandex_captcha import YandexCaptcha


class ContentTypeTuple(NamedTuple):
    """Именнованный кортеж для использования ContentType."""

    app: str
    model: str
    id: str


@shared_task
def save_remote_image(app_label: str, model: str, pk: str | int, attr_name: str, url: str) -> None:
    """Скачивание изображения из внешнего источника."""
    ct = ContentType.objects.get_by_natural_key(app_label, model)
    obj = ct.get_object_for_this_type(pk=pk)
    if not url:
        msg = "url is empty"
        raise ValueError(msg)
    if not hasattr(obj, attr_name):
        msg = f"{obj} has no attribute {attr_name}"
        raise AttributeError(msg)
    attr = getattr(obj, attr_name)
    try:
        response = requests.get(url, timeout=3)
    except requests.RequestException:
        try:
            response = requests.get(url, timeout=3)
        except requests.RequestException as e:
            sentry_sdk.capture_message(f"Error {e} {url}")
            return

    if int(response.status_code) != status.HTTP_200_OK:
        sentry_sdk.capture_message(f"Error status code {response.status_code} {url}")
        return
    image = ContentFile(response.content)
    filename = request.urlparse(url).path.split("/")[-1]
    attr.save(filename, image)


@shared_task
def convert_to_png(ctt: ContentTypeTuple, to_attr: str, url: str, width: int, height: str) -> None:
    """Конвертирование изображения в png."""
    ct = ContentType.objects.get_by_natural_key(ctt[0], ctt[1])
    obj = ct.get_object_for_this_type(pk=ctt[2])
    if not url:
        msg = "url is empty"
        raise ValueError(msg)
    if not hasattr(obj, to_attr):
        msg = f"{obj} has no attribute {to_attr}"
        raise AttributeError(msg)
    attr = getattr(obj, to_attr)
    g = requests.get(
        f"http://imgproxy:8080/signature:insecure/resize:fit:{width}:{height}:0/gravity:sm/plain/{url}@png",
        timeout=10,
    )
    g.raise_for_status()
    image = ContentFile(g.content)
    filename = f"{obj.id}_plan_png.png"
    attr.save(filename, image)


@shared_task
def send_sms(to: str, body: str) -> str:
    """Отправка SMS кода."""
    message = SMSCSMS(to=to, body=body)
    message.send()


@shared_task
def task_reset_yandex_captcha_counter() -> None:
    """Сброс количества yandex captcha."""
    YandexCaptcha().reset_yandex_captcha_counter()
