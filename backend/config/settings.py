"""Settings."""

import sys
from os import environ, getenv
from pathlib import Path
from sys import argv

from django.utils.translation import gettext_lazy as _

from common.json_celery_logging.formatter import CustomJSONFormatter

SITE_HOST = getenv("SITE_HOST")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = getenv("SECRET_KEY")

TESTING = "test" in argv or any("pytest" in a for a in argv)
DEBUG = getenv("DEBUG", "True") == "True" and not TESTING
API_DOCS_ENABLE = getenv("API_DOCS_ENABLE", "False") == "True"

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = [f"https://{SITE_HOST}"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
    "django.forms",
    # Third partry
    "solo",
    "robots",
    "ckeditor",
    "django_filters",
    "adminsortable2",
    "drf_spectacular",
    "ckeditor_uploader",
    "django_admin_listfilter_dropdown",
    "django_user_agents",
    "rest_framework",
    "location_field.apps.DefaultConfig",
    "djcelery_email",
    "django_jsonform",
    # apps
    "common.apps.CommonConfig",
    "sitemap.apps.SitemapConfig",
    "users.apps.UserConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "common.middleware.GetIPMiddleware",
]
if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar_callback(_: None) -> bool:
        """Показ дебаг панели."""
        return DEBUG

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": "config.settings.show_toolbar_callback"}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_NAME"),
        "USER": getenv("POSTGRES_USER"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST", "db"),
        "PORT": getenv("POSTGRES_PORT"),
        "CONN_MAX_AGE": 600,
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

USE_TZ = True
USE_L10N = True
USE_I18N = True
LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
LANGUAGES = (("ru", _("Russian")), ("en", _("English")))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/s/"
STATIC_ROOT = Path(BASE_DIR) / "static"

# Media
MEDIA_URL = "/m/"
MEDIA_ROOT = Path(BASE_DIR) / "media"

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755
FILE_UPLOAD_PERMISSIONS = 0o644
DATA_UPLOAD_MAX_NUMBER_FILES = 50000
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CKEditor
CKEDITOR_UPLOAD_PATH = "u/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar_Custom": [
            {"name": "document", "items": ["Source"]},
            {
                "name": "clipboard",
                "items": [
                    "Cut",
                    "Copy",
                    "Paste",
                    "PasteText",
                    "PasteFromWord",
                    "-",
                    "Undo",
                    "Redo",
                ],
            },
            {
                "name": "paragraph",
                "items": [
                    "NumberedList",
                    "BulletedList",
                    "-",
                    "Outdent",
                    "Indent",
                    "-",
                    "Blockquote",
                    "-",
                    "JustifyLeft",
                    "JustifyCenter",
                    "JustifyRight",
                    "JustifyBlock",
                ],
            },
            {"name": "links", "items": ["Link", "Unlink", "Anchor"]},
            {"name": "insert", "items": ["Table", "HorizontalRule", "SpecialChar"]},
            "/",
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {
                "name": "basicstyles",
                "items": [
                    "Bold",
                    "Italic",
                    "Underline",
                    "Strike",
                    "Subscript",
                    "Superscript",
                    "-",
                    "RemoveFormat",
                ],
            },
            {"name": "colors", "items": ["TextColor", "BGColor"]},
        ],
        "toolbar": "Custom",
        "extraPlugins": ["liststyle"],
    },
}

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    "DEFAULT_AUTHENTICATION_CLASSES": ["rest_framework.authentication.SessionAuthentication"],
    "EXCEPTION_HANDLER": "common.exception_handler.exception_handler",
}
if not DEBUG or not API_DOCS_ENABLE:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": CustomJSONFormatter,
        },
    },
    "handlers": {
        "json_stream": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "celery": {
            "handlers": ["json_stream"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Email
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = getenv("EMAIL_HOST")
EMAIL_PORT = int(getenv("EMAIL_PORT", "25"))
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_SUBJECT_PREFIX = "Template project: "
SERVER_EMAIL = getenv("SERVER_EMAIL") or EMAIL_HOST_USER

CELERY_TASK_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_RESULT_SERIALIZER = "json"
CELERY_BROKER_URL = f"redis://{getenv('REDIS_HOST', 'redis')!s}:{getenv('REDIS_PORT', 6379)!s}/0"  # noqa: PLW1508
CELERY_RESULT_BACKEND = (
    f"redis://{getenv('REDIS_HOST', 'redis')!s}:{getenv('REDIS_PORT', 6379)!s}/0"  # noqa: PLW1508
)
if TESTING:
    CELERY_EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

AUTH_USER_MODEL = "user.User"
# SMS
SMS_DEBUG = DEBUG or TESTING
SMSC_BASE_URL = "https://smsc.ru/sys/send.php"
SMSC_LOGIN = getenv("SMSC_LOGIN")
SMSC_PASSWORD = getenv("SMSC_PASSWORD")

if "SENTRY_DSN" in environ:
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=environ["SENTRY_DSN"],
        environment=environ.get("SENTRY_ENVIRONMENT"),
        traces_sample_rate=1.0,
        integrations=[DjangoIntegration(), CeleryIntegration()],
    )

if not TESTING:
    CACHES = {"default": {"BACKEND": "redis_cache.RedisCache", "LOCATION": "redis:6379"}}

SESSION_COOKIE_AGE = 31_536_000
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

ROBOTS_USE_HOST = True
ROBOTS_USE_SITEMAP = True
ROBOTS_CACHE_TIMEOUT = None
ROBOTS_SITE_BY_REQUEST = True
ROBOTS_SITEMAP_VIEW_NAME = "sitemap"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "users.backends.phone.PhoneBackend",
    "users.backends.email.EmailBackend",
]

# Django location_field
LOCATION_FIELD_PATH = "/s/" + "location_field"
LOCATION_FIELD = {
    "map.provider": "google",
    "map.zoom": 13,
    "search.provider": "google",
    "search.suffix": "",
    # Google
    "provider.google.api": "//maps.google.com/maps/api/js?sensor=false",
    "provider.google.api_key": "",
    "provider.google.api_libraries": "",
    "provider.google.map.type": "ROADMAP",
    # Mapbox
    "provider.mapbox.access_token": "",
    "provider.mapbox.max_zoom": 18,
    "provider.mapbox.id": "mapbox.streets",
    # OpenStreetMap
    "provider.openstreetmap.max_zoom": 18,
    # misc
    "resources.root_path": LOCATION_FIELD_PATH,
    "resources.media": {
        "js": (LOCATION_FIELD_PATH + "/js/form.js",),
    },
}

# Кастомный пользователь
AUTH_USER_MODEL = "users.User"
# Сайт
SITE_ID = 1

# imgproxy
IMGPROXY_SITE_HOST = getenv("IMGPROXY_SITE_HOST")
IMGPROXY_FULL_PATH = f"http://{IMGPROXY_SITE_HOST}/proxy"  # При необходимости нужно поменять
IMGPROXY_KEY = getenv("IMGPROXY_KEY")
IMGPROXY_SALT = getenv("IMGPROXY_SALT")
IMGPROXY_SECURE = False
if IMGPROXY_KEY and IMGPROXY_SALT:
    IMGPROXY_SECURE = True

# S3
AWS_ACCESS_KEY_ID = getenv("YND_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = getenv("YND_SECRET_ACCESS_KEY", None)
AWS_STORAGE_BUCKET_NAME = getenv("YND_STORAGE_BUCKET_NAME", None)
AWS_S3_ENDPOINT_URL = "https://storage.yandexcloud.net"
AWS_DEFAULT_ACL = None
AWS_LOCATION = getenv("YND_LOCATION", "media")
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

if TESTING or (
    AWS_ACCESS_KEY_ID is None or AWS_SECRET_ACCESS_KEY is None or AWS_STORAGE_BUCKET_NAME is None
):
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    BASE_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
else:
    DEFAULT_FILE_STORAGE = "common.storages.HashedFilenameS3Boto3Storage"
    BASE_FILE_STORAGE = "common.storages.CustomS3Boto3Storage"

# Yandex CAPTCHA
YND_CAPTCHA_SERVER_KEY = getenv("YND_CAPTCHA_SERVER_KEY", None)

# Django JSONSchemaForm
DJANGO_JSONFORM = {"FILE_HANDLER": "/json-file-handler/"}
