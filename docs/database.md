# Настройки базы данных

### Кейс №1

Если возникла ошибка
```shell
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 84, in _execute
    with self.db.wrap_database_errors:
  File "/usr/local/lib/python3.11/site-packages/django/db/utils.py", line 91, in __exit__
    raise dj_exc_value.with_traceback(traceback) from exc_value
  File "/usr/local/lib/python3.11/site-packages/django/db/backends/utils.py", line 87, in _execute
    return self.cursor.execute(sql)
           ^^^^^^^^^^^^^^^^^^^^^^^^
django.db.utils.ProgrammingError: operator class "gin_trgm_ops" does not exist for access method "gin"
```

То нужно установить расширение в БД, с помощью комманды

```sql
CREATE EXTENSION pg_trgm;
```
