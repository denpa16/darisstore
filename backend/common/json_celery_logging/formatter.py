from logging import LogRecord

from django.utils.timezone import now
from json_log_formatter import JSONFormatter

BUILTIN_ATTRS = {  # исключенные значения
    "args",
    "asctime",
    "created",
    "filename",
    "funcName",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


class CustomJSONFormatter(JSONFormatter):
    """Класс для переопределения методов форматера."""

    def json_record(self, message: str, extra: dict, record: LogRecord) -> dict:
        """Преобразование существующих полей."""
        extra["message"] = message
        if "time" not in extra:
            extra["time"] = now().isoformat()

        if record.exc_info:
            extra["exc_info"] = self.formatException(record.exc_info)

        return extra

    def format(self, record: LogRecord) -> dict:
        """Format."""
        message = record.getMessage()
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        if mutated_record is None:
            mutated_record = json_record
        return self.to_json(mutated_record)

    def extra_from_record(self, record: LogRecord) -> dict:
        """Исключение значений по умолчанию."""
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name not in BUILTIN_ATTRS
        }
