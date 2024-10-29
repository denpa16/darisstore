import logging
from typing import Any

from celery import Task

logger = logging.getLogger("celery")


class CustomTaskJson(Task):
    """Класс который можно использовать для полного переопределения логов."""

    def on_success(
        self,
        retval: str,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> None:
        """On_success."""
        super().on_success(retval, task_id, args, kwargs)

    def on_failure(
        self,
        exc: Exception,
        task_id: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        einfo: str,
    ) -> None:
        """On_failure."""
        super().on_failure(exc, task_id, args, kwargs, einfo)
