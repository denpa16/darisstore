# Сайт Спортивного клуба ШАГ

***

## Приложения и доступы

Development (branch **master**)

| №   | Сайт             | Название | Логин:Пароль |
|-----|------------------|----------|--------------|
| 1.  | https://skshag.ru| Сайт     |              |


## [Инструкция по pre-commit](docs/pre-commit.md)

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

STORAGE_ACCESS_KEY_ID=
STORAGE_SECRET_ACCESS_KEY=
STORAGE_BUCKET_NAME=
STORAGE_ENDPOINT_URL=
```

## ENV-файл Frontend
```shell
SITE_HOST=localhost
HTPASSWD_MODE=off
TLS_MODE=off
SENTRY_ENV=local
SERVER_API_URL=https://tourmetria.tsacloud.com/
PROXY_URL=https://tourmetria.tsacloud.com/
IMGPROXY_SITE_HOST=https://tourmetria.tsacloud.com/proxy

```
