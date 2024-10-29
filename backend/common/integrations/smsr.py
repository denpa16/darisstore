import requests
import sentry_sdk
from django.conf import settings


class SMSExceptionError(Exception):
    """Ошибка SMS."""


class SMS:
    """SMSC."""

    def __init__(
        self,
        to: str,
        body: str,
        username: str | None = None,
        password: str | None = None,
        base_url: str | None = settings.SMSC_BASE_URL,
    ) -> None:
        """Инициализация."""
        self.base_url = base_url
        if not all([username, password]):
            msg = "Set beeline username and password"
            raise SMSExceptionError(msg)
        self.username = username
        self.password = password
        self.to = to
        self.body = body

    def send(self) -> str:
        """Отправка."""
        url = (
            f"{settings.SMSC_BASE_URL}"
            f"?login={self.username}&psw={self.password}&phones={self.to}&mes={self.body}"
        )
        resp = requests.get(url)
        if resp.ok:
            try:
                return resp.text.split("-")[2].strip()
            except Exception as e:
                sentry_sdk.capture_message(
                    f"Ошибка в сервисе отправки смс\t{resp.text}\tException:{e}",
                )
        else:
            resp.raise_for_status()
            return None


class SMSCSMS(SMS):
    """Класс для SMSC."""

    def __init__(self, to, body) -> None:
        """Инициализация."""
        super().__init__(
            to=to,
            body=body,
            username=settings.SMSC_LOGIN,
            password=settings.SMSC_PASSWORD,
        )
