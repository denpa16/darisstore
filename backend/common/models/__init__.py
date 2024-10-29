from .drf_tracking_log import APIRequestLog
from django.db import connection, models
from django.db.models.signals import pre_migrate


def app_pre_migration(sender, app_config, **kwargs):
    cur = connection.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")


pre_migrate.connect(app_pre_migration)
