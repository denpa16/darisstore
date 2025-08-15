import json
from typing import NoReturn

import requests
import sentry_sdk
from django.core.cache import cache
from rest_framework import status
from rest_framework.exceptions import APIException

from config.settings import YND_CAPTCHA_SERVER_KEY

CAPTCHA_SERVER_URL = "https://captcha-api.yandex.ru/validate"


class YandexCaptchaError(APIException):
    status_code = 400

    def __init__(self, detail: str = ..., code: str = ...) -> NoReturn:
        """init."""
        super().__init__(detail, code)


class YandexCaptcha:
    def __init__(
        self, server_url: str = CAPTCHA_SERVER_URL, server_key: str = YND_CAPTCHA_SERVER_KEY,
    ) -> NoReturn:
        """init."""
        self.server_url = server_url
        self.server_key = server_key

    @staticmethod
    def increase_yandex_captcha_counter() -> NoReturn:
        """Считаем кол-во обращений к сервису яндекс капчи.

        Обновляю счетчик каждый месяц при помощи селери задачи - reset_yandex_captcha_counter.
        """
        yandex_captcha_counter = cache.get("yandex_captcha_counter")
        if yandex_captcha_counter:
            cache.incr("yandex_captcha_counter")
        cache.set("yandex_captcha_counter", 1)

    @staticmethod
    def reset_yandex_captcha_counter() -> NoReturn:
        yandex_captcha_counter = cache.get("yandex_captcha_counter")
        if yandex_captcha_counter:
            cache.delete("yandex_captcha_counter")

    @staticmethod
    def get_yandex_captcha_counter() -> int:
        yandex_captcha_counter: int = cache.get("yandex_captcha_counter")
        return yandex_captcha_counter

    def check_captcha(self, token: str, ip_address: str) -> bool:
        """Проверяем пользователя по ip с капчей.И увеличиваем каунтер обращений к апи яндекса."""
        if not all([self.server_key, self.server_url]):
            raise YandexCaptchaError(detail="Yandex captcha not initialized")
        try:
            resp: requests.Response = requests.get(
                self.server_url,
                {"secret": self.server_key, "token": token, "ip": ip_address},
                timeout=1,
            )

            self.increase_yandex_captcha_counter()

            if resp.status_code != status.HTTP_200_OK:
                raise YandexCaptchaError(detail="Yandex error")
            return json.loads(resp.content.decode()).get("status") == "ok"
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            sentry_sdk.capture_exception(e)
            return False
