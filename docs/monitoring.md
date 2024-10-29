# Настройка мониторинга на проектах

## Сылки на наши ресурсы для мониторинга

1. Sentry - http://sentry.idacloud.ru/
2. prometheus - https://prometheus.idacloud.ru/
3. alertmanager - https://alertmanager.idacloud.ru/#/alerts
4. grafana - https://grafana.idacloud.ru . Что бы получить доступ, напишите своему тимлиду

### На данный момент у нас обязательны следующие виды мониторинга:

1. [Sentry](http://sentry.idacloud.ru/) - мониторинг ошибок в приложении
2. [Node Exporter](https://github.com/prometheus/node_exporter) - мониторинг ресурсов сервера или ноды
3. [Cadvisor](https://github.com/google/cadvisor) - мониторинг ресурсов докера. Позволяет отследить нагрузку по каждому
   контейнеру
4. [pg_stat](https://registry.hub.docker.com/r/bitnami/postgres-exporter) - мониторинг нагруженности БД

### Также будут полезными следующие мониторинги, _на больших проектах они обязательны_:

1. [Loki](https://grafana.com/oss/loki/) - агрегатор логов. С помощью него можно довольно быстро искать данные по логам
   приложения, и выводить различную статистику
2. Celery - мониторинг celery
   тасок. [
   Реализуется с помощью Flower](https://flower.readthedocs.io/en/latest/prometheus-integration.html#configure-prometheus-to-scrape-flower-metrics)
3. Nginx - можно отследить статистику по Nginx, но глобально бесполезен.

## Как мне добавить мониторинг на свой проект?

P.S. весь мониторинг нужно публикровать под паролем, т.е. с помощью nginx закрывать доступы с помощь basic авторизации.

### [Sentry](http://sentry.idacloud.ru/)

Что бы добавить мониторинг ошибок в sentry, вы можете просто создать проект в http://sentry.idacloud.ru/, или попросить
это сделать старшего разработчика или тимлида. Далее вы добавляете sentry_dsn (по факту это url, на который будут
слаться ошибки)
в переменную **SENTRY_DSN** в переменные **CI\CD** . И все, далее сработает магия шаблонного проекта, и у вас
автоматически подключится sentry.

### [Node Exporter](https://github.com/prometheus/node_exporter)

Для подключения достаточно добавить сервис в docker-compose файл. На примере шаблонного приложения, сервис добавлен в
файле **docker-compose.production.yml**, под названием **node-exporter**.

Далее вам нужно добавить настройку в nginx, чтобы данные были доступны "из вне". Пример конфигурации можно посмотреть в
файле **exporters.conf** (которая находиться в папке **nginx**), который далее
инклюдиться в **nginx.conf.esh**

### [Cadvisor](https://github.com/google/cadvisor)

Подключение такое же, как и для **Node Exporter**. Пример можно посмотреть в **docker-compose.production.yml** и в **
exporters.conf**

### [pg_stat](https://registry.hub.docker.com/r/bitnami/postgres-exporter)

Подключение такое же, как и для **Node Exporter**. Пример можно посмотреть в **docker-compose.production.yml** и в **
exporters.conf**.

Так же для работы pg_stat нужно подключить модуль в базе. Делается это просто, можете посмотреть пример конфигурации
базы в
**docker-compose.production.yml**

Кроме этого, есть еще расширение `pg_stat_statements`, которое также нужно подключить в  **docker-compose.production.yml**

После проливки нужно будет один раз подключиться напрямую к БД и выполнить команду

```postgresql
create extension pg_stat_statements;
```
С этого момента база начнет собирать статистику по запросам

### Loki

**Loki** - система хранения и обработки логов. Доступна в [graphana](https://grafana.idacloud.ru).
Для запуска сборки логов, нужно добавить в env переменные:

```
LOKI_URL=https://loki.idacloud.ru/loki/api/v1/push
LOKI_USERNAME=<логин>
LOKI_PASSWORD=<пароль>
LOKI_SERVER_TAG=<слаг проекта>
```

Далее нужно подключить `promtail` - сервис, который будет собирать логи из journald и отправлять их в локи.

**Важно**, логи желательно выдавать в формате json.

#### Обработка логов для статистики

Promtail позволяет проводить предобработку логов перед отправкой в loki, например, группировать запросы по url.
Для этого он их параметризует, то есть заменяет числовой id или uuid в адресе на `<id>`.
Это позволяет в дальнейшем собирать статистику по группа запросов.

Для правильной работы этого функционала необходимо настроить `gunicorn`, чтобы он выдавал логи в формате json.
Для этого нужно в сервисе backend в команде запуска gunicorn добавить параметр `--access-logformat`

```yaml
command: >
          gunicorn config.wsgi:application -w ${GUNICORN_WORKERS:-8} -t 120 --keep-alive 120 -b 0.0.0.0:8000 --access-logfile - --error-logfile -
          --access-logformat '{"date":"%(t)s","method":"%(m)s","path":"%(U)s","query":"%(q)s","protocol":"%(H)s","status":%(s)s,"response_size":%(B)s,"referer":"%(f)s","user_agent":"%(a)s","time":%(D)s,"ip":"%({x-real-ip}i)s"}'
```

### [Celery](https://flower.readthedocs.io/en/latest/prometheus-integration.html#configure-prometheus-to-scrape-flower-metrics)

Для начала нужно поставить контейнер с [Flower](https://flower.readthedocs.io/en/latest/). Он предоставляет визуальный
инструмент для отслеживания задач celery, но также собирает статистику и метрики. Метрики подключаются из коробки. Но
нужно открыть flower для доступа "из вне", для этого нужно прописать конфигурацию в **nginx.conf.esh**

## И так, вы сделали все необходимое, а как сделать что бы все заработало?

У нас реализована автоматическая генерация конфигурации мониторинга (т.е. конфигурации prometheus и alertmanager), чтобы
все подтянулось и все завелось - нужно написать вашему тимлиду, что бы он обновил конфигурацию.
