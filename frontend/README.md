# Структура базового проекта Nuxt.js:

| Директория     | Описание                                                                                                                           |
|----------------|------------------------------------------------------------------------------------------------------------------------------------|
| `./`           | Корневые файлы [README_FILES.md](README_FILES.md)                                                                                  |
| `/assets/`     | Содержит нескомпилированные файлы с исходным кодом глобальных стилей, скриптов, шрифтов и картинок [README.md](./assets/README.md) |
| `/components/` | Директория, в которой хранятся все компоненты проекта, от страничный блоков до ui-компонентов  [README.md](./components/README.md) |
| `/config/`     | Включается в себя различные файлы конфигурации, которые подключается в **nuxt.config.js** [README.md](./config/README.md)          |
| `/directives/` | Для хранения кастомных vue директив [README.md](./directives/README.md)                                                            |
| `/layouts/`    | Содержит компоненты для определения шаблонов страниц [README.md](./layouts/README.md)                                              |
| `/mixins/`     | Для хранения миксинов приложения [README.md](./mixins/README.md)                                                                   |
| `/pages/`      | Содержит компоненты страниц [README.md](./pages/README.md)                                                                         |
| `/static/`     | Содержит статические файлы. Каждый файл в этой папке доступен через `/` [README.md](./static/README.md)                            |
| `/store/`      | Содержит файлы **Vuex** хранилища [README.md](./store/README.md)                                                                   |


# Запуск приложения

Требуемая версия **node v20.3.0** и **npm 9.6.7**.
[Подробности как переключать версии с помощью nvm](https://www.notion.so/idaproject/node-npm-a730b66532aa494388f968bf4e07aa97)

## Устанавливаем зависимости

```
npm install
```

## Добавляем `env` переменные в `.env` файл

```
PROXY_URL - ссылка на api для локального запуска (напр: https://site.com)
SERVER_API_URL - ссылка на контейнер с api для серверной части (напр: https://backend:8000)
CLIENT_API_URL - ссылка на api на клиенте (напр: https://site.com)
SENTRY_DSN - ключ Sentry для проекта для логирования ошибок (для локальной разработки нет необходимости)
IMGPROXY_SITE_HOST - Для корректной работы imgProxy (напр: https://site.com/proxy)
GTM=False - Если требуется отключить метрики
UI_DEMO=True - Для включения расширинной визуализации кита, с примерами кода и описанием пропсов/методов/эмитов и т.п.
```

При SSR запросы будут отправляться на адрес, указанный в **PROXY_URL**. При CSR запросы отправляются
на **location.origin** и разрешаются с помощью проксирования. Настройки прокси можно посмотреть
в **config/proxy.js**.

`SERVER_API_URL`, `CLIENT_API_URL`, `SENTRY_DSN` переменные, для работы с локальным, окружением - **добавлять не нужно**.

## `.env` файл для текущего проекта
```
IMGPROXY_SITE_HOST=https://template.idacloud.ru/proxy
PROXY_URL=https://template.idacloud.ru/
UI_DEMO=True
```

## Запускаем проект в `dev` режиме

```
npm run dev
```

## Запускаем проект в `prod` режиме

```
npm run build && npm run start
```

## Для ручного запуска проверки линтеров

```
npm run lint:fix
```

## Для анализа размера бандла

```
npm run analyze
```
[Документация по работе с ImgProxy](https://www.notion.so/idaproject/Nuxt-image-ImgProxy-new-0ec9ed96ed3e4fb983c8cb632dd289a0)

[Frontend Best-Practice](https://www.notion.so/idaproject/Best-practice-455b95c9b4414c91bc71c039c33230cb)
