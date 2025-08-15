from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db import models
from django.db.models.functions import Upper

User = get_user_model()


class PrefetchUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("user")


class APIRequestLog(models.Model):
    """Логирует зопросы к Django REST Framework API."""

    objects = PrefetchUserManager()

    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    username_persistent = models.CharField(
        verbose_name="Имя пользователя",
        max_length=getattr(settings, "DRF_TRACKING_USERNAME_LENGTH", 200),
        null=True,
        blank=True,
        help_text="Поле сохраняется даже если объект пользователя удален",
        db_index=True,
    )
    requested_at = models.DateTimeField(verbose_name="Дата и время запроса", db_index=True)
    response_ms = models.PositiveIntegerField(verbose_name="Время выполнения кода представления, мс", default=0)
    path = models.CharField(
        verbose_name="URL запроса",
        max_length=getattr(settings, "DRF_TRACKING_PATH_LENGTH", 200),
        db_index=True,
    )
    view = models.CharField(
        verbose_name="View запроса",
        max_length=getattr(settings, "DRF_TRACKING_VIEW_LENGTH", 200),
        null=True,
        blank=True,
        db_index=True,
    )
    view_method = models.CharField(
        verbose_name="View-метод запроса",
        max_length=getattr(settings, "DRF_TRACKING_VIEW_METHOD_LENGTH", 200),
        null=True,
        blank=True,
        db_index=True,
    )
    remote_addr = models.GenericIPAddressField(verbose_name="IP-адрес источника запроса", db_index=True)
    host = models.URLField(verbose_name="Хост", db_index=True)
    method = models.CharField(verbose_name="Метод запроса", max_length=10, db_index=True)
    query_params = models.TextField(verbose_name="Параметры запроса", null=True, blank=True)
    data = models.TextField(verbose_name="Данные", null=True, blank=True)
    response = models.TextField(verbose_name="Ответ", null=True, blank=True)
    errors = models.TextField(verbose_name="Ошибки", null=True, blank=True)
    status_code = models.PositiveIntegerField(verbose_name="Статус ответа", null=True, blank=True, db_index=True)

    class Meta:
        verbose_name = "Лог запроса к DRF API"
        verbose_name_plural = "Логи запросов к DRF API"
        indexes = (
            models.Index(Upper("username_persistent"), name="username_persistent_idx"),
            GinIndex(
                fields=["username_persistent"],
                opclasses=["gin_trgm_ops"],
                name="username_persistent_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("username_persistent"), name="gin_trgm_ops"),
                name="username_persistent_up_gin_idx",
            ),
            models.Index(Upper("path"), name="path_idx"),
            GinIndex(
                fields=["path"],
                opclasses=["gin_trgm_ops"],
                name="path_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("path"), name="gin_trgm_ops"),
                name="path_up_gin_idx",
            ),
            models.Index(Upper("view"), name="view_idx"),
            GinIndex(
                fields=["view"],
                opclasses=["gin_trgm_ops"],
                name="view_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("view"), name="gin_trgm_ops"),
                name="view_upper_gin_idx",
            ),
            models.Index(Upper("view_method"), name="view_method_idx"),
            GinIndex(
                fields=["view_method"],
                opclasses=["gin_trgm_ops"],
                name="view_method_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("view_method"), name="gin_trgm_ops"),
                name="view_method_upper_gin_idx",
            ),
            models.Index(Upper("host"), name="host_idx"),
            GinIndex(
                fields=["host"],
                opclasses=["gin_trgm_ops"],
                name="host_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("host"), name="gin_trgm_ops"),
                name="host_upper_gin_idx",
            ),
            models.Index(Upper("method"), name="method_idx"),
            GinIndex(
                fields=["method"],
                opclasses=["gin_trgm_ops"],
                name="method_gin_idx",
            ),
            GinIndex(
                OpClass(Upper("method"), name="gin_trgm_ops"),
                name="method_upper_gin_idx",
            ),
        )

    def __str__(self):
        return f"{self.method} {self.path}"
