from typing import TYPE_CHECKING, NoReturn

from rest_framework.fields import CharField

if TYPE_CHECKING:
    from rest_framework.request import Request

from typing import Any

from .yandex_captcha import YandexCaptcha, YandexCaptchaError


class YandexCaptchaField(CharField):
    def get_attribute(self, _: Any) -> None:
        return None


class YandexCaptchaMixin:
    yandex_token = YandexCaptchaField(label="Токен для Яндекс.Капча", required=True)

    def __init__(self, *args: list, **kwargs: dict) -> NoReturn:
        """Init."""
        self.fields.update(
            {"yandex_token": YandexCaptchaField(label="Токен для Яндекс.Капча", required=True)},
        )
        super().__init__(*args, **kwargs)

    def validate(self, attrs: dict) -> dict:
        """validate."""
        yandex_token = attrs.get("yandex_token")
        request: Request = self.context.get("request")
        ip = request.ip
        if ip and yandex_token:
            check = YandexCaptcha().check_captcha(yandex_token, ip)
            if not check:
                raise YandexCaptchaError(detail="Captcha check failed")
        else:
            raise YandexCaptchaError(detail="Wrong ip or yandex_token")
        attrs.pop("yandex_token")
        return super().validate(attrs)
