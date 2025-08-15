import requests
import sentry_sdk
from django.conf import settings


class SMSException(Exception):
    pass


class SMS:
    def __init__(
        self,
        to: str,
        body: str,
        username: str | None = None,
        password: str | None = None,
        base_url: str | None = settings.SMSC_BASE_URL,
    ) -> None:
        self.base_url = base_url
        if not all([username, password]):
            raise SMSException("Set beeline username and password")
        self.username = username
        self.password = password
        self.to = to
        self.body = body

    def send(self) -> str:
        url = f"{settings.SMSC_BASE_URL}?login={self.username}&psw={self.password}&phones={self.to}&mes={self.body}"
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
    def __init__(self, to, body):
        super().__init__(
            to=to,
            body=body,
            username=settings.SMSC_LOGIN,
            password=settings.SMSC_PASSWORD,
        )
