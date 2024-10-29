## ВАЖНО!
## Перед началом работы

### 1. Установить pre-commit. При нелинтованном коде - пайплайны упадут и деплоя не произойдет
### [Инструкция по pre-commit](docs/pre-commit.md)
### 2. Порог покрытия тестов > 96%. При меньшем проценте покрытия - пайплайны упадут и деплоя не произойдет
### Запуск тестов локально
```shell
make tests c="app_name"
```
## Локальный запуск приложения
### Не забудьте создать файл .env

```shell
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --remove-orphans -d --build

если вышла ошибка сборки контейнера - поднять его отдельно

docker-compose build backend

затем снова поднять все контейнеры

docker-compose -f docker-compose.yml -f docker-compose.override.yml up --remove-orphans -d --build
```




## ENV-файл Backend
```shell
SITE_HOST=localhost
DEBUG=True

# Если есть mkcert, то можете прокинуть свои локальные сертификаты в nginx,
# тем самым подняв https соединение на локалке. Если не хочется этим заниматься,
# то поставьте переменную TLS_MODE=off, и заходите на проект по http://localhost:8000
TLS_MODE=off
TLS_CERTIFICATE=.certs/localhost.pem
TLS_CERTIFICATE_KEY=.certs/localhost-key.pem

SECRET_KEY=my_very_sercet_key

POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
POSTGRES_NAME=postgres
POSTGRES_USER=postgres

YND_ACCESS_KEY_ID=
YND_S3_ENDPOINT_URL=https://storage.yandexcloud.net/
YND_SECRET_ACCESS_KEY=
YND_STORAGE_BUCKET_NAME=

# Imageproxy
IMGPROXY_SITE_HOST=img.localhost
IMGPROXY_DEVELOPMENT_ERRORS_MODE=false
IMGPROXY_IGNORE_SSL_VERIFICATION=false
IMGPROXY_SALT=
IMGPROXY_KEY=
# imgproxy s3
IMGPROXY_S3_ENDPOINT=https://storage.yandexcloud.net/
IMGPROXY_ALLOWED_SOURCES=

# SMS
WEBSMS_LOGIN=
WEBSMS_PASSWORD=
```
