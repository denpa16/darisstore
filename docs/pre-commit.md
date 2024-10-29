# Настройка pre-commit

Необходимо глобально установить pre-commit

```shell
pip install --break-system-packages pre-commit
```

В папке проекта выполните следующую команду,
чтобы производились проверки перед каждым коммитом:

```shell
pre-commit autoupdate && pre-commit install && pre-commit install --install-hooks && pre-commit install --hook-type commit-msg
```

Pre-commit запускается авторматически при коммите.

Ручной запуск pre-commit

```shell
pre-commit run --all-files
```
