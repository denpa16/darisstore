# PROJECT_NAME

***

## Приложения и доступы

### Flow ведения проекта: [Feature branch](https://www.notion.so/idaproject/Git-73fbbfc1392245c7b0cc7cbedd904ba4#157af0b196194f46b52a449685dd54d4) \ [Git Flow](https://www.notion.so/idaproject/Git-73fbbfc1392245c7b0cc7cbedd904ba4#3c3375bad3d74b27966556b2cd1bfddc)

Production (branch **master**):

| №   | Сайт                                                                                 | Название        | Логин:Пароль |
|-----|--------------------------------------------------------------------------------------|-----------------|--------------|
| 1.  | https://glorax.com                                                                   | Общий сайт      |
| 2.  | https://manager.glorax.com                                                           | Менеджер панель |              |
| 3.  | https://glorax.com/flower/                                                           | Flower          |              |

Development (branch **dev**):

| №   | Сайт                                                                                 | Название        | Логин:Пароль |
|-----|--------------------------------------------------------------------------------------|-----------------|--------------|
| 1.  | https://glorax.idacloud.ru                                                           | Общий сайт      |
| 2.  | https://panel.glorax.idacloud.ru/                                                    | Менеджер панель |              |

***

## Локальный запуск приложения

```shell
docker-compose build
# Не забудьте создать файл .env
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --remove-orphans -d --build
```

## ENV

### Backend

```shell
SITE_HOST=localhost
DEBUG=False

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

# Для каждого проекта создается storage в Яндекс.Облако.
# Что бы его создать, попросите лида создать его, он вам недостающие данные вышлет.
AWS_ACCESS_KEY_ID=
AWS_S3_ENDPOINT_URL=https://storage.yandexcloud.net/
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# imgproxy
IMGPROXY_SITE_HOST=img.localhost
IMGPROXY_DEVELOPMENT_ERRORS_MODE=false
IMGPROXY_IGNORE_SSL_VERIFICATION=false
IMGPROXY_SALT=87738d552fbb7e54c0976d84268659647ba3e5af16e6b5fac7206c77a1e52efe875fd585ca60882beb96e9526df35b9288f679149592acd6bcfec2ddfd29f350
IMGPROXY_KEY=2eb8f2f5cb67e1628e9e2bce3ab71e6c27cb467e92156a2ce39cbe6e828f01992fe8658e19adff8c017d745c4332e5c0e1679fb3bff3faa748c43ae0b527c854
# imgproxy s3
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
IMGPROXY_S3_ENDPOINT=https://storage.yandexcloud.net/
IMGPROXY_ALLOWED_SOURCES=

```

### Frontend

```shell
SERVER_API_URL=https://project.idacloud.ru
PROXY_URL=https://project.idacloud.ru
GTM=False #для отключения метрик
```

***

## Документация

### [API Swagger](https://www.google.com/)

> Данные для входа на документацию: <strong>gloraxdocs:ida223322</strong>

### [Notion проекта](https://www.notion.so/idaproject/70bc10c60c5f428a88b462163a00db46)
