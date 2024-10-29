import os

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()
app.conf.beat_schedule = {}


@setup_logging.connect
def config_loggers(*args, **kwags) -> None:
    """Подключение логов в Celery."""
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)


if __name__ == "__main__":
    app.start()
