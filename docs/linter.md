# Настройка линтеров

1. Установить через `poetry`актуальные зависимости разработки `[tool.poetry.dev-dependencies]`
  (Можно посмотреть в проекте `template_project`)

2. Проверить настройки black, isort в файле `pyproject.toml`

3. Проверить настройки flake8, mypy в файле `setup.cfg`

4. Протестировать линтеры через ручной запуск `pre-commit`


```shell
pre-commit run --all-files
```
